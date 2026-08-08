from __future__ import annotations

import json
from pathlib import Path
import re

from .reconciliation import validate_canonical_inventory, validate_reconciliation_manifest


ALLOWED_STATUSES = {"ported", "planned", "blocked"}
ALLOWED_PORT_KINDS = {"native", "workflow-adapted", "runtime-aware", "hand-port-enhanced"}
ALLOWED_CAPABILITY_STATUSES = {"integrated", "external", "tracked", "deferred", "rejected"}
ALLOWED_INTEGRATION_MODES = {"codex-adapted", "external-runtime", "tracking-only"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
AUTHORING_HOME_PATTERN = re.compile(r"/(?:Users|home)/")
BACKTICKED_SKILL_PATTERN = r"`[a-z0-9]+(?:-[a-z0-9]+)*`"
SKILL_REFERENCE_CLUSTER_PATTERN = (
    rf"{BACKTICKED_SKILL_PATTERN}"
    rf"(?:\s*(?:,\s*(?:(?:or|and)\s+)?|(?:or|and)\s+){BACKTICKED_SKILL_PATTERN})*"
)
REQUIRED_DOCS = (
    Path("docs/idea-strategy.md"),
    Path("docs/product-strategy.md"),
    Path("docs/implementation-strategy.md"),
    Path("docs/mvp-plan.md"),
    Path("docs/gbrain-adaptation-memo.md"),
    Path("docs/gbrain-import-inventory.md"),
    Path("docs/gbrain-compatibility-map.md"),
    Path("docs/gbrain-resolver.md"),
    Path("docs/codex-brain-substrate.md"),
    Path("docs/codex-host-refresh-audit.md"),
    Path("docs/codex-documentation-refresh.md"),
    Path("docs/upstream-runtime-deepening-pass.md"),
    Path("docs/adoption-examples.md"),
    Path("docs/compatibility-map.md"),
    Path("docs/runtime-compatibility.md"),
    Path("docs/upstream-parity-2026-07-16.md"),
    Path("docs/impeccable-compatibility-map.md"),
    Path("docs/impeccable-adoption-report-2026-07-16.md"),
    Path("docs/coding-workflow.md"),
    Path("docs/release-checklist.md"),
    Path("docs/reconciliation-alpha.md"),
    Path("docs/reconciliation-beta.md"),
    Path("docs/reconciliation-complete.md"),
    Path("docs/engineering-milestone-alpha.md"),
)
REQUIRED_PACKAGE_FILES = (
    Path("CONTRIBUTING.md"),
    Path("SECURITY.md"),
    Path("CHANGELOG.md"),
    Path("LICENSE"),
    Path("LICENSES/Apache-2.0.txt"),
    Path(".github/CODEOWNERS"),
    Path(".github/workflows/ci.yml"),
    Path("scripts/install_skills.py"),
    Path("scripts/smoke_install.py"),
    Path("scripts/check_public_boundary.py"),
    Path("scripts/build_skill_inventory.py"),
    Path("scripts/build_complete_reconciliation.py"),
    Path("scripts/record_skill_review.py"),
    Path("scripts/refresh_reconciliation_manifest.py"),
    Path("scripts/check_engineering_milestone.py"),
    Path("data/canonical-skill-inventory.json"),
    Path("data/reconciliation-alpha.json"),
    Path("data/reconciliation-beta.json"),
    Path("data/reconciliation-complete.json"),
    Path("data/reconciliation-record.schema.json"),
)
SKILL_MAP_FILES = (
    Path("data/skill-map.json"),
    Path("data/gbrain-skill-map.json"),
    Path("data/praneet-skill-map.json"),
)
CAPABILITY_MAP_FILES = (Path("data/impeccable-capability-map.json"),)


def load_skill_map(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_source_commit(skill_map: dict, skill: dict) -> str:
    return str(
        skill.get("source_commit")
        or skill_map["source"].get("skill_parity_commit")
        or skill_map["source"]["commit"]
    )


def skill_reviewed_commit(skill_map: dict, skill: dict) -> str:
    """Return the latest upstream boundary reviewed for one skill.

    Adoption and review are intentionally separate. A Codex adapter may retain
    its current implementation after a newer Claude-specific upstream change
    has been reviewed and explicitly deferred.
    """

    return str(
        skill.get("reviewed_commit")
        or skill_map["source"].get("skill_reviewed_commit")
        or skill_source_commit(skill_map, skill)
    )


def capability_source_commit(capability_map: dict, capability: dict) -> str:
    return str(
        capability.get("source_commit")
        or capability_map["source"].get("capability_parity_commit")
        or capability_map["source"]["commit"]
    )


def short_commit(commit: str) -> str:
    return commit[:7]


def extract_frontmatter_keys(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    keys: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return keys
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        keys[key.strip()] = value.strip()

    return {}


def extract_routed_skill_references(text: str) -> set[str]:
    """Return explicit backticked skill names from routing instructions.

    This deliberately ignores ordinary prose and shell commands. Router sections
    and lines that explicitly say to use, route to, or invoke a skill are the
    portable cross-skill contract that an exported package must preserve.
    """

    references: set[str] = set()
    in_routing_section = False

    for line in text.splitlines():
        if line.startswith("## "):
            in_routing_section = bool(re.search(r"\brouting\b", line, re.IGNORECASE))
            continue

        if in_routing_section:
            routing_clause = re.split(r"\s+with\s+the\b", line, maxsplit=1, flags=re.IGNORECASE)[0]
            candidates = re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", routing_clause)
        else:
            match = re.search(
                rf"\b(?:use|invoke)\s+({SKILL_REFERENCE_CLUSTER_PATTERN})",
                line,
                re.IGNORECASE,
            )
            if not match:
                match = re.search(
                    rf"\broute\b.*?\bto\s+({SKILL_REFERENCE_CLUSTER_PATTERN})",
                    line,
                    re.IGNORECASE,
                )
            candidates = (
                re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", match.group(1))
                if match
                else []
            )

        for candidate in candidates:
            if SKILL_NAME_PATTERN.fullmatch(candidate):
                references.add(candidate)

    return references


def validate_skill_portability(skill_md: Path, skill_names: set[str]) -> list[str]:
    """Check the portable contract for a single reusable skill."""

    errors: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter_keys(text)
    expected_name = skill_md.parent.name
    relative_path = skill_md.as_posix()

    if frontmatter.get("name") != expected_name:
        errors.append(
            f"{relative_path} has name={frontmatter.get('name')!r}; expected {expected_name!r}."
        )
    if not frontmatter.get("description"):
        errors.append(f"{relative_path} is missing a description frontmatter field.")
    if not SKILL_NAME_PATTERN.fullmatch(expected_name):
        errors.append(f"{relative_path} uses a non-portable skill name: {expected_name!r}.")
    if "user-invocable" in frontmatter:
        errors.append(
            f"{relative_path} uses non-portable user-invocable frontmatter; keep exportable metadata portable."
        )
    if AUTHORING_HOME_PATTERN.search(text):
        errors.append(
            f"{relative_path} embeds an authoring-machine absolute home path; resolve it from runtime context instead."
        )

    for target in sorted(extract_routed_skill_references(text)):
        if target not in skill_names:
            errors.append(f"{relative_path} routes to missing skill: {target!r}.")

    return errors


def validate_skill_map(data: dict) -> list[str]:
    errors: list[str] = []

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("Missing top-level source object in a skill map file.")
    else:
        for key in ("name", "repo", "license", "commit"):
            if not source.get(key):
                errors.append(f"Missing source.{key} in a skill map file.")
        parity_commit = source.get("skill_parity_commit")
        if parity_commit is not None and (
            not isinstance(parity_commit, str) or len(parity_commit.strip()) < 7
        ):
            errors.append(
                f"Invalid source.skill_parity_commit {parity_commit!r}; "
                "expected a git commit SHA string."
            )
        reviewed_commit = source.get("skill_reviewed_commit")
        if reviewed_commit is not None and (
            not isinstance(reviewed_commit, str) or len(reviewed_commit.strip()) < 7
        ):
            errors.append(
                f"Invalid source.skill_reviewed_commit {reviewed_commit!r}; "
                "expected a git commit SHA string."
            )

    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append("Each skill map file must include a non-empty skills list.")
        return errors

    seen_upstream: set[str] = set()
    seen_codex: set[str] = set()
    for index, skill in enumerate(skills, start=1):
        if not isinstance(skill, dict):
            errors.append(f"Skill entry #{index} is not an object.")
            continue

        upstream_slug = skill.get("upstream_slug")
        codex_slug = skill.get("codex_slug")
        status = skill.get("status")
        port_kind = skill.get("port_kind")
        summary = skill.get("summary")
        notes = skill.get("notes")
        source_files = skill.get("source_files")
        source_commit = skill.get("source_commit")
        reviewed_commit = skill.get("reviewed_commit")

        if not upstream_slug:
            errors.append(f"Skill entry #{index} is missing upstream_slug.")
        if not codex_slug:
            errors.append(f"Skill entry #{index} is missing codex_slug.")
        if status not in ALLOWED_STATUSES:
            errors.append(
                f"Skill entry #{index} has invalid status {status!r}; "
                f"expected one of {sorted(ALLOWED_STATUSES)}."
            )
        if port_kind not in ALLOWED_PORT_KINDS:
            errors.append(
                f"Skill entry #{index} has invalid port_kind {port_kind!r}; "
                f"expected one of {sorted(ALLOWED_PORT_KINDS)}."
            )
        if not summary:
            errors.append(f"Skill entry #{index} is missing summary.")
        if not notes:
            errors.append(f"Skill entry #{index} is missing notes.")
        if not isinstance(source_files, list) or not source_files:
            errors.append(f"Skill entry #{index} needs at least one source_files entry.")
        if source_commit is not None:
            if not isinstance(source_commit, str) or len(source_commit.strip()) < 7:
                errors.append(
                    f"Skill entry #{index} has invalid source_commit {source_commit!r}; "
                    "expected a git commit SHA string."
                )
        if reviewed_commit is not None:
            if not isinstance(reviewed_commit, str) or len(reviewed_commit.strip()) < 7:
                errors.append(
                    f"Skill entry #{index} has invalid reviewed_commit {reviewed_commit!r}; "
                    "expected a git commit SHA string."
                )

        if upstream_slug:
            if upstream_slug in seen_upstream:
                errors.append(f"Duplicate upstream slug: {upstream_slug}.")
            seen_upstream.add(upstream_slug)

        if codex_slug:
            if codex_slug in seen_codex:
                errors.append(f"Duplicate codex slug: {codex_slug}.")
            seen_codex.add(codex_slug)

    return errors


def validate_capability_map(data: dict) -> list[str]:
    errors: list[str] = []

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("Missing top-level source object in a capability map file.")
    else:
        for key in ("name", "repo", "license", "commit"):
            if not source.get(key):
                errors.append(f"Missing source.{key} in a capability map file.")
        parity_commit = source.get("capability_parity_commit")
        if parity_commit is not None and (
            not isinstance(parity_commit, str) or len(parity_commit.strip()) < 7
        ):
            errors.append(
                f"Invalid source.capability_parity_commit {parity_commit!r}; "
                "expected a git commit SHA string."
            )

    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("Each capability map file must include a non-empty capabilities list.")
        return errors

    seen_ids: set[str] = set()
    for index, capability in enumerate(capabilities, start=1):
        if not isinstance(capability, dict):
            errors.append(f"Capability entry #{index} is not an object.")
            continue

        capability_id = capability.get("id")
        status = capability.get("status")
        integration_mode = capability.get("integration_mode")
        upstream_paths = capability.get("upstream_paths")
        local_targets = capability.get("local_targets")

        if not capability_id:
            errors.append(f"Capability entry #{index} is missing id.")
        elif capability_id in seen_ids:
            errors.append(f"Duplicate capability id: {capability_id}.")
        else:
            seen_ids.add(capability_id)

        if status not in ALLOWED_CAPABILITY_STATUSES:
            errors.append(
                f"Capability entry #{index} has invalid status {status!r}; "
                f"expected one of {sorted(ALLOWED_CAPABILITY_STATUSES)}."
            )
        if integration_mode not in ALLOWED_INTEGRATION_MODES:
            errors.append(
                f"Capability entry #{index} has invalid integration_mode {integration_mode!r}; "
                f"expected one of {sorted(ALLOWED_INTEGRATION_MODES)}."
            )
        if not capability.get("summary"):
            errors.append(f"Capability entry #{index} is missing summary.")
        if not capability.get("notes"):
            errors.append(f"Capability entry #{index} is missing notes.")
        if not isinstance(upstream_paths, list) or not upstream_paths:
            errors.append(f"Capability entry #{index} needs at least one upstream_paths entry.")
        if not isinstance(local_targets, list):
            errors.append(f"Capability entry #{index} needs a local_targets list.")

        source_commit = capability.get("source_commit")
        if source_commit is not None and (
            not isinstance(source_commit, str) or len(source_commit.strip()) < 7
        ):
            errors.append(
                f"Capability entry #{index} has invalid source_commit {source_commit!r}; "
                "expected a git commit SHA string."
            )

    return errors


def validate_repo(repo_root: Path) -> list[str]:
    errors: list[str] = []

    for rel_path in REQUIRED_DOCS:
        if not (repo_root / rel_path).exists():
            errors.append(f"Missing required documentation file: {rel_path}.")

    for rel_path in REQUIRED_PACKAGE_FILES:
        if not (repo_root / rel_path).exists():
            errors.append(f"Missing required package file: {rel_path}.")

    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        errors.append("Missing README.md.")

    skill_mds = sorted((repo_root / "skills").glob("*/SKILL.md"))
    skill_names = {skill_md.parent.name for skill_md in skill_mds}
    for skill_md in skill_mds:
        errors.extend(validate_skill_portability(skill_md, skill_names))

    for skill_map_rel in SKILL_MAP_FILES:
        skill_map_path = repo_root / skill_map_rel
        if not skill_map_path.exists():
            errors.append(f"Missing {skill_map_rel}.")
            continue

        skill_map = load_skill_map(skill_map_path)
        errors.extend(validate_skill_map(skill_map))

        for skill in skill_map.get("skills", []):
            if skill.get("status") != "ported":
                continue

            codex_slug = skill["codex_slug"]
            skill_md = repo_root / "skills" / codex_slug / "SKILL.md"
            if not skill_md.exists():
                errors.append(f"Ported skill is missing SKILL.md: skills/{codex_slug}/SKILL.md.")
                continue

            for source_file in skill.get("source_files", []):
                source_path = repo_root / "skills" / source_file
                if not source_path.exists():
                    errors.append(f"Missing ported skill source file: skills/{source_file}.")

    for capability_map_rel in CAPABILITY_MAP_FILES:
        capability_map_path = repo_root / capability_map_rel
        if not capability_map_path.exists():
            errors.append(f"Missing {capability_map_rel}.")
            continue

        capability_map = load_skill_map(capability_map_path)
        errors.extend(validate_capability_map(capability_map))
        for capability in capability_map.get("capabilities", []):
            for local_target in capability.get("local_targets", []):
                if not (repo_root / local_target).exists():
                    errors.append(
                        f"Capability {capability.get('id')!r} references missing local target: "
                        f"{local_target}."
                    )

    inventory_path = repo_root / "data" / "canonical-skill-inventory.json"
    if inventory_path.exists():
        inventory = load_skill_map(inventory_path)
        errors.extend(validate_canonical_inventory(inventory, repo_root))
        reconciliation_paths = sorted((repo_root / "data").glob("reconciliation-*.json"))
        for reconciliation_path in reconciliation_paths:
            if reconciliation_path.name.endswith(".schema.json"):
                continue
            reconciliation = load_skill_map(reconciliation_path)
            errors.extend(
                validate_reconciliation_manifest(reconciliation, repo_root, inventory)
            )

    return errors


def format_status_table(data: dict) -> str:
    rows = [
        (
            skill["upstream_slug"],
            skill["codex_slug"],
            skill["status"],
            skill["port_kind"],
            short_commit(skill_source_commit(data, skill)),
            skill["summary"],
        )
        for skill in data["skills"]
    ]

    widths = [len("Upstream"), len("Codex"), len("Status"), len("Port kind"), len("Source"), len("Summary")]
    for upstream, codex, status, port_kind, source, summary in rows:
        widths[0] = max(widths[0], len(upstream))
        widths[1] = max(widths[1], len(codex))
        widths[2] = max(widths[2], len(status))
        widths[3] = max(widths[3], len(port_kind))
        widths[4] = max(widths[4], len(source))
        widths[5] = max(widths[5], len(summary))

    def render(row: tuple[str, str, str, str, str, str]) -> str:
        return (
            f"{row[0]:<{widths[0]}}  "
            f"{row[1]:<{widths[1]}}  "
            f"{row[2]:<{widths[2]}}  "
            f"{row[3]:<{widths[3]}}  "
            f"{row[4]:<{widths[4]}}  "
            f"{row[5]:<{widths[5]}}"
        )

    header = render(("Upstream", "Codex", "Status", "Port kind", "Source", "Summary"))
    divider = render(tuple("-" * width for width in widths))
    body = "\n".join(render(row) for row in rows)
    return "\n".join((header, divider, body))


def format_capability_status_table(data: dict) -> str:
    rows = [
        (
            capability["id"],
            capability["status"],
            capability["integration_mode"],
            short_commit(capability_source_commit(data, capability)),
            capability["summary"],
        )
        for capability in data["capabilities"]
    ]

    widths = [len("Capability"), len("Status"), len("Mode"), len("Source"), len("Summary")]
    for capability_id, status, mode, source, summary in rows:
        widths[0] = max(widths[0], len(capability_id))
        widths[1] = max(widths[1], len(status))
        widths[2] = max(widths[2], len(mode))
        widths[3] = max(widths[3], len(source))
        widths[4] = max(widths[4], len(summary))

    def render(row: tuple[str, str, str, str, str]) -> str:
        return (
            f"{row[0]:<{widths[0]}}  "
            f"{row[1]:<{widths[1]}}  "
            f"{row[2]:<{widths[2]}}  "
            f"{row[3]:<{widths[3]}}  "
            f"{row[4]:<{widths[4]}}"
        )

    header = render(("Capability", "Status", "Mode", "Source", "Summary"))
    divider = render(tuple("-" * width for width in widths))
    body = "\n".join(render(row) for row in rows)
    return "\n".join((header, divider, body))
