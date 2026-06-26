from __future__ import annotations

import json
from pathlib import Path


ALLOWED_STATUSES = {"ported", "planned", "blocked"}
ALLOWED_PORT_KINDS = {"native", "workflow-adapted", "runtime-aware", "hand-port-enhanced"}
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
    Path("docs/adoption-examples.md"),
    Path("docs/compatibility-map.md"),
    Path("docs/runtime-compatibility.md"),
)
SKILL_MAP_FILES = (
    Path("data/skill-map.json"),
    Path("data/gbrain-skill-map.json"),
    Path("data/praneet-skill-map.json"),
)


def load_skill_map(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_source_commit(skill_map: dict, skill: dict) -> str:
    return str(skill.get("source_commit") or skill_map["source"]["commit"])


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


def validate_skill_map(data: dict) -> list[str]:
    errors: list[str] = []

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("Missing top-level source object in a skill map file.")
    else:
        for key in ("name", "repo", "license", "commit"):
            if not source.get(key):
                errors.append(f"Missing source.{key} in a skill map file.")

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

        if upstream_slug:
            if upstream_slug in seen_upstream:
                errors.append(f"Duplicate upstream slug: {upstream_slug}.")
            seen_upstream.add(upstream_slug)

        if codex_slug:
            if codex_slug in seen_codex:
                errors.append(f"Duplicate codex slug: {codex_slug}.")
            seen_codex.add(codex_slug)

    return errors


def validate_repo(repo_root: Path) -> list[str]:
    errors: list[str] = []

    for rel_path in REQUIRED_DOCS:
        if not (repo_root / rel_path).exists():
            errors.append(f"Missing required documentation file: {rel_path}.")

    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        errors.append("Missing README.md.")

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

            frontmatter = extract_frontmatter_keys(skill_md.read_text(encoding="utf-8"))
            if frontmatter.get("name") != codex_slug:
                errors.append(
                    f"skills/{codex_slug}/SKILL.md has name={frontmatter.get('name')!r}; "
                    f"expected {codex_slug!r}."
                )
            if not frontmatter.get("description"):
                errors.append(f"skills/{codex_slug}/SKILL.md is missing a description frontmatter field.")

            for source_file in skill.get("source_files", []):
                source_path = repo_root / "skills" / source_file
                if not source_path.exists():
                    errors.append(f"Missing ported skill source file: skills/{source_file}.")

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
