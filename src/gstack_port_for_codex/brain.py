from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from html import unescape
from pathlib import Path
import hashlib
import json
import os
import re
import shutil


DEFAULT_BRAIN_ROOT = Path("brain")
BRAIN_DIRS = (
    "people",
    "companies",
    "concepts",
    "ideas",
    "originals",
    "sources",
    "meetings",
    "reports",
)
CATEGORY_ALIASES = {
    "person": "people",
    "people": "people",
    "company": "companies",
    "companies": "companies",
    "concept": "concepts",
    "concepts": "concepts",
    "idea": "ideas",
    "ideas": "ideas",
    "original": "originals",
    "originals": "originals",
    "source": "sources",
    "sources": "sources",
    "meeting": "meetings",
    "meetings": "meetings",
    "report": "reports",
    "reports": "reports",
}
PAGE_TYPES = {
    "people": "person",
    "companies": "company",
    "concepts": "concept",
    "ideas": "idea",
    "originals": "original",
    "sources": "source",
    "meetings": "meeting",
    "reports": "report",
}
WORD_RE = re.compile(r"[a-z0-9]+")
CITATION_RE = re.compile(r"\[Source:\s*[^\]]+\]")
CITATION_PREFIX_RE = re.compile(r"\[(?i:source)\s*:")
HTML_TAG_RE = re.compile(r"<[^>]+>")
CAPITALIZED_ENTITY_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\b")
WHITESPACE_RE = re.compile(r"[ \t]+")
COMMON_ENTITY_STOP_WORDS = {
    "And",
    "But",
    "For",
    "From",
    "I",
    "If",
    "In",
    "It",
    "The",
    "This",
    "That",
    "They",
    "We",
    "When",
}
SYNC_MANAGED_KIND = "mutable-source-v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class BrainPage:
    path: Path
    category: str
    slug: str
    title: str
    page_type: str
    frontmatter: dict[str, str]
    compiled_truth: str
    timeline: str
    body: str


@dataclass(frozen=True)
class SearchHit:
    path: Path
    title: str
    score: int
    snippet: str


@dataclass(frozen=True)
class CitationIssue:
    path: Path
    line_number: int
    issue: str
    line: str


@dataclass(frozen=True)
class SourceSyncResult:
    path: Path
    source_path: Path
    status: str
    version: int
    source_sha256: str


def slugify(text: str) -> str:
    tokens = WORD_RE.findall(text.lower())
    if not tokens:
        return "untitled"
    return "-".join(tokens)


def ensure_brain_root(brain_root: Path) -> None:
    brain_root.mkdir(parents=True, exist_ok=True)
    for directory in BRAIN_DIRS:
        (brain_root / directory).mkdir(parents=True, exist_ok=True)
    (brain_root / ".raw").mkdir(parents=True, exist_ok=True)
    (brain_root / "_dead-letter").mkdir(parents=True, exist_ok=True)


def normalize_category(category: str) -> str:
    normalized = CATEGORY_ALIASES.get(category.strip().lower())
    if normalized is None:
        raise ValueError(f"Unknown brain category: {category}")
    return normalized


def page_type_for_category(category: str) -> str:
    normalized = normalize_category(category)
    return PAGE_TYPES[normalized]


def _extract_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    frontmatter: dict[str, str] = {}
    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        stripped = line.strip()
        if stripped == "---":
            end_index = index
            break
        if not stripped or ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()

    if end_index is None:
        return {}, text

    body = "\n".join(lines[end_index + 1 :]).strip()
    return frontmatter, body


def parse_brain_page(path: Path) -> BrainPage:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = _extract_frontmatter(text)
    compiled_truth, timeline = _split_compiled_truth_and_timeline(body)
    title = frontmatter.get("title") or _fallback_title(path, compiled_truth)
    page_type = frontmatter.get("type") or page_type_for_category(path.parent.name)

    return BrainPage(
        path=path,
        category=path.parent.name,
        slug=path.stem,
        title=title,
        page_type=page_type,
        frontmatter=frontmatter,
        compiled_truth=compiled_truth.strip(),
        timeline=timeline.strip(),
        body=body.strip(),
    )


def _fallback_title(path: Path, compiled_truth: str) -> str:
    for line in compiled_truth.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped:
            return stripped[:80]
    return path.stem.replace("-", " ").title()


def _split_compiled_truth_and_timeline(body: str) -> tuple[str, str]:
    separator = "\n---\n"
    if separator not in body:
        return body, ""
    compiled_truth, timeline = body.split(separator, 1)
    return compiled_truth, timeline


def iter_brain_pages(brain_root: Path) -> list[BrainPage]:
    if not brain_root.exists():
        return []

    pages: list[BrainPage] = []
    for path in sorted(brain_root.rglob("*.md")):
        if path.name == "README.md":
            continue
        if path.parent == brain_root:
            continue
        if path.parent.name not in BRAIN_DIRS:
            continue
        pages.append(parse_brain_page(path))
    return pages


def search_brain(brain_root: Path, query: str, limit: int = 10) -> list[SearchHit]:
    tokens = WORD_RE.findall(query.lower())
    if not tokens:
        return []

    hits: list[SearchHit] = []
    for page in iter_brain_pages(brain_root):
        score = _score_page(page, tokens)
        if score <= 0:
            continue
        hits.append(
            SearchHit(
                path=page.path,
                title=page.title,
                score=score,
                snippet=_snippet_for_page(page, tokens),
            )
        )

    return sorted(
        hits,
        key=lambda hit: (-hit.score, str(hit.path)),
    )[:limit]


def _score_page(page: BrainPage, tokens: list[str]) -> int:
    title_counts = Counter(WORD_RE.findall(page.title.lower()))
    path_counts = Counter(WORD_RE.findall(str(page.path).lower()))
    body_counts = Counter(WORD_RE.findall(page.body.lower()))

    score = 0
    for token in tokens:
        score += title_counts[token] * 6
        score += path_counts[token] * 3
        score += body_counts[token]

    if all(token in body_counts or token in title_counts or token in path_counts for token in tokens):
        score += 4
    return score


def _snippet_for_page(page: BrainPage, tokens: list[str], width: int = 160) -> str:
    for line in page.body.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if stripped and any(token in lowered for token in tokens):
            return stripped[:width]

    text = page.compiled_truth.strip() or page.timeline.strip()
    return text[:width]


def format_search_hits(hits: list[SearchHit], brain_root: Path) -> str:
    if not hits:
        return "No brain hits."

    lines: list[str] = []
    for index, hit in enumerate(hits, start=1):
        rel_path = hit.path.relative_to(brain_root.parent if brain_root.name == DEFAULT_BRAIN_ROOT.name else brain_root)
        lines.append(f"{index}. {hit.title} [{rel_path}] score={hit.score}")
        if hit.snippet:
            lines.append(f"   {hit.snippet}")
    return "\n".join(lines)


def brain_stats(brain_root: Path) -> dict[str, object]:
    pages = iter_brain_pages(brain_root)
    by_category = Counter(page.category for page in pages)
    return {
        "brain_root": str(brain_root),
        "page_count": len(pages),
        "categories": dict(sorted(by_category.items())),
    }


def validate_brain(brain_root: Path) -> list[str]:
    errors: list[str] = []
    for directory in BRAIN_DIRS:
        if not (brain_root / directory).exists():
            errors.append(f"Missing brain directory: {directory}.")

    for page in iter_brain_pages(brain_root):
        if not page.title.strip():
            errors.append(f"{page.path} is missing a title.")
        if not page.compiled_truth.strip():
            errors.append(f"{page.path} is missing compiled truth.")
        if not page.frontmatter.get("type"):
            errors.append(f"{page.path} is missing frontmatter type.")

    return errors


def make_page_path(brain_root: Path, category: str, title: str) -> Path:
    normalized = normalize_category(category)
    return brain_root / normalized / f"{slugify(title)}.md"


def render_page(
    title: str,
    page_type: str,
    compiled_truth: str,
    timeline_entries: list[str] | None = None,
    tags: list[str] | None = None,
) -> str:
    tag_text = ", ".join(tags or [])
    timeline_text = "\n".join(timeline_entries or [])
    return (
        "---\n"
        f"title: {title}\n"
        f"type: {page_type}\n"
        f"tags: [{tag_text}]\n"
        "---\n\n"
        f"{compiled_truth.strip()}\n\n"
        "---\n\n"
        f"{timeline_text.strip()}\n"
    )


def report_as_json(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def parse_tags(frontmatter_tags: str | None) -> list[str]:
    if not frontmatter_tags:
        return []
    text = frontmatter_tags.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [part.strip() for part in text.split(",") if part.strip()]


def merge_tags(*tag_lists: list[str]) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for tag_list in tag_lists:
        for tag in tag_list:
            if tag not in seen:
                seen.add(tag)
                merged.append(tag)
    return merged


def split_timeline_entries(timeline: str) -> list[str]:
    return [line.strip() for line in timeline.splitlines() if line.strip()]


def merge_timeline_entries(existing: list[str], additions: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for entry in additions:
        if entry not in seen:
            merged.append(entry)
            seen.add(entry)
    return merged


def merge_compiled_truth(existing: str, addition: str) -> str:
    existing = existing.strip()
    addition = addition.strip()
    if not existing:
        return addition
    if not addition or addition in existing:
        return existing
    return f"{existing}\n\n{addition}"


def upsert_page(
    brain_root: Path,
    category: str,
    title: str,
    compiled_truth: str,
    timeline_entries: list[str] | None = None,
    tags: list[str] | None = None,
    page_type: str | None = None,
) -> Path:
    ensure_brain_root(brain_root)
    normalized = normalize_category(category)
    path = make_page_path(brain_root, normalized, title)
    entry_lines = [entry.strip() for entry in timeline_entries or [] if entry.strip()]

    if path.exists():
        page = parse_brain_page(path)
        merged_truth = merge_compiled_truth(page.compiled_truth, compiled_truth)
        merged_timeline = merge_timeline_entries(split_timeline_entries(page.timeline), entry_lines)
        merged_tags = merge_tags(parse_tags(page.frontmatter.get("tags")), tags or [])
        type_value = page.page_type or page_type or page_type_for_category(normalized)
        rendered = render_page(
            page.title or title,
            type_value,
            merged_truth,
            merged_timeline,
            merged_tags,
        )
    else:
        rendered = render_page(
            title,
            page_type or page_type_for_category(normalized),
            compiled_truth,
            entry_lines,
            tags,
        )

    path.write_text(rendered, encoding="utf-8")
    return path


def resolve_page_reference(brain_root: Path, reference: str, *, category: str | None = None) -> Path | None:
    candidate = Path(reference)
    if candidate.suffix == ".md":
        if candidate.is_absolute() and candidate.exists():
            return candidate
        repo_relative = brain_root.parent / candidate
        if repo_relative.exists():
            return repo_relative

    normalized = slugify(reference)
    pages = iter_brain_pages(brain_root)
    if category is not None:
        desired = normalize_category(category)
        pages = [page for page in pages if page.category == desired]

    for page in pages:
        if page.slug == normalized:
            return page.path
        if page.title.lower() == reference.lower():
            return page.path
    return None


def append_timeline_entry(path: Path, entry: str) -> bool:
    if not entry.strip():
        return False

    page = parse_brain_page(path)
    timeline_entries = merge_timeline_entries(split_timeline_entries(page.timeline), [entry.strip()])
    rendered = render_page(
        page.title,
        page.page_type,
        page.compiled_truth,
        timeline_entries,
        parse_tags(page.frontmatter.get("tags")),
    )
    changed = rendered != path.read_text(encoding="utf-8")
    if changed:
        path.write_text(rendered, encoding="utf-8")
    return changed


def relative_page_link(from_path: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_path.parent)


def make_backlink_entry(target_path: Path, referencing_path: Path, event_date: str, context: str) -> str:
    referencing_page = parse_brain_page(referencing_path)
    rel_link = relative_page_link(target_path, referencing_path)
    clean_context = context.strip().rstrip(".")
    return (
        f"- {event_date}: Referenced in [{referencing_page.title}]({rel_link})"
        f" - {clean_context}. [Source: linked brain page, {event_date}]"
    )


def add_backlink(target_path: Path, referencing_path: Path, event_date: str, context: str) -> bool:
    entry = make_backlink_entry(target_path, referencing_path, event_date, context)
    return append_timeline_entry(target_path, entry)


def preserve_raw_text(brain_root: Path, owner_slug: str, name: str, text: str) -> Path:
    ensure_brain_root(brain_root)
    raw_dir = brain_root / ".raw" / owner_slug
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / name
    target.write_text(text, encoding="utf-8")
    return target


def preserve_raw_file(brain_root: Path, owner_slug: str, source_path: Path) -> Path:
    ensure_brain_root(brain_root)
    raw_dir = brain_root / ".raw" / owner_slug
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / source_path.name
    shutil.copy2(source_path, target)
    return target


def sanitize_external_text(text: str) -> str:
    text = unescape(text)
    text = HTML_TAG_RE.sub(" ", text)
    lines = [WHITESPACE_RE.sub(" ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def detect_capitalized_entities(text: str) -> list[str]:
    entities: list[str] = []
    seen: set[str] = set()
    for match in CAPITALIZED_ENTITY_RE.finditer(text):
        entity = match.group(0).strip()
        if entity in COMMON_ENTITY_STOP_WORDS:
            continue
        if entity not in seen:
            seen.add(entity)
            entities.append(entity)
    return entities


def normalize_citation_markup(text: str) -> str:
    text = re.sub(r"\[(?i:source)\s*:", "[Source:", text)
    text = re.sub(r"\[Source:\s+", "[Source: ", text)
    text = re.sub(r"\s+\]", "]", text)
    return text


def audit_citations(brain_root: Path) -> list[CitationIssue]:
    issues: list[CitationIssue] = []
    for page in iter_brain_pages(brain_root):
        issues.extend(_audit_page_citations(page))
    return issues


def _audit_page_citations(page: BrainPage) -> list[CitationIssue]:
    issues: list[CitationIssue] = []
    for line_number, line in enumerate(page.body.splitlines(), start=1):
        stripped = line.strip()
        if not _line_requires_citation(stripped):
            continue
        if CITATION_RE.search(stripped):
            continue
        if CITATION_PREFIX_RE.search(stripped):
            issues.append(CitationIssue(page.path, line_number, "malformed-citation", stripped))
            continue
        issues.append(CitationIssue(page.path, line_number, "missing-citation", stripped))
    return issues


def _line_requires_citation(line: str) -> bool:
    if not line:
        return False
    if line.startswith(("---", "#", ">", "|", "```")):
        return False
    if not any(char.isalpha() for char in line):
        return False
    if line.startswith("- "):
        return True
    return len(line) >= 24


def rewrite_citation_markup(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    normalized = normalize_citation_markup(text)
    if normalized == text:
        return 0
    path.write_text(normalized, encoding="utf-8")
    return 1


def default_today() -> str:
    return datetime.now().date().isoformat()


def _validate_sync_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"Sync date must use YYYY-MM-DD: {value}") from exc


def _decode_frontmatter_string(value: str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"Managed source projection is missing {field_name} metadata.")
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        decoded = value
    if not isinstance(decoded, str) or not decoded.strip():
        raise ValueError(f"Managed source projection has invalid {field_name} metadata.")
    return decoded


def _parse_source_version(value: str | None) -> int:
    if value is None:
        raise ValueError("Managed source projection is missing source_version metadata.")
    try:
        version = int(value)
    except ValueError as exc:
        raise ValueError("Managed source projection has invalid source_version metadata.") from exc
    if version < 1:
        raise ValueError("Managed source projection has invalid source_version metadata.")
    return version


def _quote_source_projection(source_text: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in source_text.rstrip("\n").splitlines())


def _render_source_projection(
    *,
    title: str,
    page_type: str,
    tags: list[str],
    source_path: Path,
    source_sha256: str,
    source_version: int,
    first_synced: str,
    last_changed: str,
    supersedes_sha256: str | None,
    source_text: str,
    timeline_entries: list[str],
) -> str:
    tag_text = ", ".join(tags)
    path_text = json.dumps(str(source_path), ensure_ascii=False)
    supersedes_text = supersedes_sha256 or "none"
    citation = f"[Source: synchronized local file, {last_changed}]"
    compiled_truth = "\n".join(
        (
            f"**Source path:** {path_text} {citation}",
            f"**Current SHA-256:** `{source_sha256}` {citation}",
            f"**Source version:** {source_version} {citation}",
            f"**First synchronized:** {first_synced} {citation}",
            f"**Last changed:** {last_changed} {citation}",
            f"**Supersedes SHA-256:** `{supersedes_text}` {citation}",
            "",
            "## Current Source Projection",
            "",
            _quote_source_projection(source_text),
        )
    )
    timeline_text = "\n".join(timeline_entries)
    return (
        "---\n"
        f"title: {title}\n"
        f"type: {page_type}\n"
        f"tags: [{tag_text}]\n"
        f"sync_managed: {json.dumps(SYNC_MANAGED_KIND)}\n"
        f"source_path: {path_text}\n"
        f"source_sha256: {source_sha256}\n"
        f"source_version: {source_version}\n"
        f"first_synced: {first_synced}\n"
        f"last_changed: {last_changed}\n"
        f"supersedes_sha256: {supersedes_text}\n"
        "---\n\n"
        f"{compiled_truth.strip()}\n\n"
        "---\n\n"
        f"{timeline_text.strip()}\n"
    )


def sync_source_projection(
    brain_root: Path,
    input_path: Path,
    *,
    title: str | None = None,
    category: str = "sources",
    sync_date: str | None = None,
    tags: list[str] | None = None,
) -> SourceSyncResult:
    """Synchronize one mutable UTF-8 source into a managed local brain page.

    The current compiled truth is replaced when the source hash changes while
    the source-version timeline is retained. An unchanged source is a byte-for-
    byte no-op. Managed pages refuse a different source path or an unmanaged
    existing page so a title collision cannot silently overwrite local memory.
    """

    requested_path = Path(input_path).expanduser()
    try:
        source_path = requested_path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Source file does not exist: {requested_path}") from exc
    if not source_path.is_file():
        raise ValueError(f"Source path is not a regular file: {source_path}")

    source_bytes = source_path.read_bytes()
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Source file is not valid UTF-8: {source_path}") from exc
    if not source_text.strip():
        raise ValueError(f"Source file is empty: {source_path}")

    normalized_category = normalize_category(category)
    sync_day = _validate_sync_date(sync_date or default_today())
    page_title = title.strip() if title is not None else source_path.stem.replace("-", " ").replace("_", " ").title()
    if not page_title:
        raise ValueError("Source projection title must not be empty.")

    ensure_brain_root(brain_root)
    page_path = make_page_path(brain_root, normalized_category, page_title)
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    projection_tags = merge_tags(["synced-source"], tags or [])

    if not page_path.exists():
        timeline_entries = [
            f"- {sync_day}: Synchronized version 1 from {json.dumps(str(source_path), ensure_ascii=False)} "
            f"at SHA-256 `{source_sha256}`. [Source: synchronized local file, {sync_day}]"
        ]
        rendered = _render_source_projection(
            title=page_title,
            page_type=page_type_for_category(normalized_category),
            tags=projection_tags,
            source_path=source_path,
            source_sha256=source_sha256,
            source_version=1,
            first_synced=sync_day,
            last_changed=sync_day,
            supersedes_sha256=None,
            source_text=source_text,
            timeline_entries=timeline_entries,
        )
        page_path.write_text(rendered, encoding="utf-8")
        return SourceSyncResult(page_path, source_path, "created", 1, source_sha256)

    page = parse_brain_page(page_path)
    if "sync_managed" not in page.frontmatter:
        raise ValueError(f"Refusing to overwrite unmanaged brain page: {page_path}")
    managed_kind = _decode_frontmatter_string(page.frontmatter.get("sync_managed"), "sync_managed")
    if managed_kind != SYNC_MANAGED_KIND:
        raise ValueError(f"Refusing to overwrite unmanaged brain page: {page_path}")

    existing_source_path = _decode_frontmatter_string(page.frontmatter.get("source_path"), "source_path")
    if existing_source_path != str(source_path):
        raise ValueError(
            f"Managed brain page already belongs to a different source: {existing_source_path}. "
            "Choose a distinct --title."
        )

    existing_sha256 = page.frontmatter.get("source_sha256", "")
    if not SHA256_RE.fullmatch(existing_sha256):
        raise ValueError("Managed source projection has invalid source_sha256 metadata.")
    existing_version = _parse_source_version(page.frontmatter.get("source_version"))
    if existing_sha256 == source_sha256:
        return SourceSyncResult(page_path, source_path, "no-op", existing_version, source_sha256)

    first_synced = page.frontmatter.get("first_synced", "")
    _validate_sync_date(first_synced)
    new_version = existing_version + 1
    timeline_entries = split_timeline_entries(page.timeline)
    timeline_entries.append(
        f"- {sync_day}: Synchronized version {new_version} from {json.dumps(str(source_path), ensure_ascii=False)}; "
        f"superseded version {existing_version} (`{existing_sha256}`) with `{source_sha256}`. "
        f"[Source: synchronized local file, {sync_day}]"
    )
    rendered = _render_source_projection(
        title=page.title,
        page_type=page.page_type,
        tags=merge_tags(parse_tags(page.frontmatter.get("tags")), projection_tags),
        source_path=source_path,
        source_sha256=source_sha256,
        source_version=new_version,
        first_synced=first_synced,
        last_changed=sync_day,
        supersedes_sha256=existing_sha256,
        source_text=source_text,
        timeline_entries=timeline_entries,
    )
    page_path.write_text(rendered, encoding="utf-8")
    return SourceSyncResult(page_path, source_path, "updated", new_version, source_sha256)
