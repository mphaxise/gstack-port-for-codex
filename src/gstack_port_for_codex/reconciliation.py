from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess


ALLOWED_CLASSIFICATIONS = {
    "condensed",
    "host-adapted",
    "intentionally-removed",
    "local-origin",
    "obsolete",
    "preserved",
    "user-edited",
}
ALLOWED_HOST_COUPLING = {"portable", "codex-adapter", "runtime-heavy"}
ALLOWED_DECISIONS = {"adopted", "local-origin", "reviewed-deferred"}
SKILL_MAP_PATHS = (
    Path("data/skill-map.json"),
    Path("data/gbrain-skill-map.json"),
    Path("data/praneet-skill-map.json"),
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_text(content: str) -> str:
    return sha256_bytes(content.encode("utf-8"))


def normalized_line_retention(source: str, target: str) -> float:
    """Measure retained nonblank source lines without duplicate inflation."""

    def normalized_lines(text: str) -> Counter[str]:
        return Counter(line.strip() for line in text.splitlines() if line.strip())

    source_lines = normalized_lines(source)
    if not source_lines:
        return 100.0
    target_lines = normalized_lines(target)
    retained = sum((source_lines & target_lines).values())
    return round(retained * 100 / sum(source_lines.values()), 2)


def build_canonical_inventory(repo_root: Path) -> dict:
    mapped: dict[str, dict] = {}
    for map_path in SKILL_MAP_PATHS:
        data = json.loads((repo_root / map_path).read_text(encoding="utf-8"))
        source = data["source"]
        for skill in data["skills"]:
            slug = skill["codex_slug"]
            mapped[slug] = {
                "source_name": source["name"],
                "source_repo": source["repo"],
                "source_slug": skill["upstream_slug"],
                "adopted_commit": str(
                    skill.get("source_commit")
                    or source.get("skill_parity_commit")
                    or source["commit"]
                ),
                "port_kind": skill["port_kind"],
                "status": skill["status"],
            }

    entries: list[dict] = []
    for skill_md in sorted((repo_root / "skills").glob("*/SKILL.md")):
        slug = skill_md.parent.name
        content_hash = sha256_bytes(skill_md.read_bytes())
        provenance = mapped.get(slug)
        entry = {
            "canonical_id": f"skill:{slug}",
            "skill_name": slug,
            "local_path": skill_md.relative_to(repo_root).as_posix(),
            "content_sha256": content_hash,
            "content_group": f"sha256:{content_hash}",
            "owner": "portable-core",
            "adapter": "codex",
        }
        if provenance:
            entry.update(provenance)
        else:
            entry.update(
                {
                    "source_name": "local",
                    "source_repo": None,
                    "source_slug": slug,
                    "adopted_commit": None,
                    "port_kind": "local-origin",
                    "status": "ported",
                }
            )
        entries.append(entry)

    group_sizes = Counter(entry["content_group"] for entry in entries)
    for entry in entries:
        entry["exact_duplicate_group_size"] = group_sizes[entry["content_group"]]

    return {
        "schema_version": 1,
        "scope": "public-packaged-skills",
        "entries": entries,
    }


def validate_canonical_inventory(inventory: dict, repo_root: Path) -> list[str]:
    errors: list[str] = []
    if inventory.get("schema_version") != 1:
        errors.append("Canonical inventory schema_version must be 1.")
    if inventory.get("scope") != "public-packaged-skills":
        errors.append("Canonical inventory scope must be public-packaged-skills.")

    entries = inventory.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["Canonical inventory needs a non-empty entries list."]

    seen_ids: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        canonical_id = entry.get("canonical_id")
        if not canonical_id:
            errors.append(f"Canonical inventory entry #{index} is missing canonical_id.")
        elif canonical_id in seen_ids:
            errors.append(f"Duplicate canonical inventory id: {canonical_id}.")
        else:
            seen_ids.add(canonical_id)

        local_path = entry.get("local_path")
        if not local_path or not (repo_root / local_path).is_file():
            errors.append(f"Canonical inventory entry #{index} has missing local_path: {local_path!r}.")
            continue
        content_hash = sha256_bytes((repo_root / local_path).read_bytes())
        if entry.get("content_sha256") != content_hash:
            errors.append(f"Canonical inventory hash drift for {canonical_id}.")
        if entry.get("content_group") != f"sha256:{content_hash}":
            errors.append(f"Canonical inventory content group drift for {canonical_id}.")

    expected = build_canonical_inventory(repo_root)
    if inventory != expected:
        errors.append(
            "Canonical inventory is stale; run python3 scripts/build_skill_inventory.py."
        )
    return errors


def git_blob_text(repo: Path, commit: str, path: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def refresh_reconciliation_manifest(
    manifest: dict,
    repo_root: Path,
    upstream_roots: dict[str, Path],
) -> dict:
    refreshed = json.loads(json.dumps(manifest))
    sources = refreshed["sources"]

    for record in refreshed["records"]:
        local_text = (repo_root / record["local_path"]).read_text(encoding="utf-8")
        record["hashes"]["local_sha256"] = sha256_text(local_text)
        source_name = record["source_name"]
        if source_name == "local":
            record["hashes"]["adopted_source_sha256"] = None
            record["hashes"]["current_upstream_sha256"] = None
            record["retention"]["adopted_source_percent"] = None
            record["retention"]["current_upstream_percent"] = None
            continue

        source = sources[source_name]
        upstream_root = upstream_roots[source_name]
        adopted_text = git_blob_text(
            upstream_root,
            source["adopted_commit"],
            record["upstream_path"],
        )
        current_text = git_blob_text(
            upstream_root,
            source["current_commit"],
            record["upstream_path"],
        )
        record["hashes"]["adopted_source_sha256"] = sha256_text(adopted_text)
        record["hashes"]["current_upstream_sha256"] = sha256_text(current_text)
        record["retention"]["adopted_source_percent"] = normalized_line_retention(
            adopted_text,
            local_text,
        )
        record["retention"]["current_upstream_percent"] = normalized_line_retention(
            current_text,
            local_text,
        )

    return refreshed


def validate_reconciliation_manifest(
    manifest: dict,
    repo_root: Path,
    inventory: dict,
) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("Reconciliation manifest schema_version must be 1.")
    if manifest.get("milestone") != "alpha":
        errors.append("Reconciliation manifest milestone must be alpha.")

    inventory_ids = {entry["canonical_id"] for entry in inventory.get("entries", [])}
    sources = manifest.get("sources")
    if not isinstance(sources, dict) or not sources:
        errors.append("Reconciliation manifest needs source metadata.")
        sources = {}
    else:
        for source_name, source in sources.items():
            for field in ("adopted_commit", "current_commit"):
                if not COMMIT_PATTERN.fullmatch(str(source.get(field, ""))):
                    errors.append(f"Reconciliation source {source_name} has invalid {field}.")

    records = manifest.get("records")
    if not isinstance(records, list) or not records:
        return errors + ["Reconciliation manifest needs a non-empty records list."]

    seen_ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        canonical_id = record.get("canonical_id")
        if canonical_id in seen_ids:
            errors.append(f"Duplicate reconciliation record: {canonical_id}.")
        seen_ids.add(canonical_id)
        if canonical_id not in inventory_ids:
            errors.append(f"Reconciliation record is absent from inventory: {canonical_id}.")

        source_name = record.get("source_name")
        if source_name != "local" and source_name not in sources:
            errors.append(f"Unknown reconciliation source for {canonical_id}: {source_name!r}.")
        if source_name != "local" and not record.get("upstream_path"):
            errors.append(f"Reconciliation record {canonical_id} is missing upstream_path.")

        local_path = record.get("local_path")
        if not local_path or not (repo_root / local_path).is_file():
            errors.append(f"Reconciliation record {canonical_id} has missing local_path.")
            continue
        local_hash = sha256_bytes((repo_root / local_path).read_bytes())
        hashes = record.get("hashes", {})
        if hashes.get("local_sha256") != local_hash:
            errors.append(f"Reconciliation local hash drift for {canonical_id}.")
        if source_name == "local":
            if hashes.get("adopted_source_sha256") is not None:
                errors.append(f"Local-origin record {canonical_id} has an adopted source hash.")
            if hashes.get("current_upstream_sha256") is not None:
                errors.append(f"Local-origin record {canonical_id} has a current upstream hash.")
        else:
            for field in ("adopted_source_sha256", "current_upstream_sha256"):
                if not SHA256_PATTERN.fullmatch(str(hashes.get(field, ""))):
                    errors.append(f"Reconciliation record {canonical_id} has invalid {field}.")

        classifications = record.get("classifications")
        if not isinstance(classifications, list) or not classifications:
            errors.append(f"Reconciliation record {canonical_id} needs classifications.")
        else:
            invalid = sorted(set(classifications) - ALLOWED_CLASSIFICATIONS)
            if invalid:
                errors.append(f"Reconciliation record {canonical_id} has invalid classifications: {invalid}.")
        if record.get("host_coupling") not in ALLOWED_HOST_COUPLING:
            errors.append(f"Reconciliation record {canonical_id} has invalid host_coupling.")
        if record.get("decision") not in ALLOWED_DECISIONS:
            errors.append(f"Reconciliation record {canonical_id} has invalid decision.")

        removals = record.get("intentional_removals")
        if not isinstance(removals, list):
            errors.append(f"Reconciliation record {canonical_id} needs intentional_removals.")
        else:
            for removal in removals:
                if not removal.get("category") or not removal.get("reason"):
                    errors.append(f"Reconciliation record {canonical_id} has an unexplained removal.")
            if "intentionally-removed" in (classifications or []) and not removals:
                errors.append(f"Reconciliation record {canonical_id} lacks its removal manifest.")

        retention = record.get("retention", {})
        if retention.get("basis") != "normalized-nonblank-line-overlap":
            errors.append(f"Reconciliation record {canonical_id} has an unknown retention basis.")
        for field in ("adopted_source_percent", "current_upstream_percent"):
            value = retention.get(field)
            if value is not None and (not isinstance(value, (int, float)) or not 0 <= value <= 100):
                errors.append(f"Reconciliation record {canonical_id} has invalid {field}.")
            if source_name != "local" and value is None:
                errors.append(f"Reconciliation record {canonical_id} is missing {field}.")

        companions = record.get("companion_resources")
        if not isinstance(companions, list):
            errors.append(f"Reconciliation record {canonical_id} needs companion_resources.")
        else:
            for companion in companions:
                if not (repo_root / companion).exists():
                    errors.append(
                        f"Reconciliation record {canonical_id} has missing companion resource: {companion}."
                    )

        if not isinstance(record.get("validation"), list) or not record.get("validation"):
            errors.append(f"Reconciliation record {canonical_id} needs validation commands.")

    return errors
