from __future__ import annotations

import json
import os
import shutil
import ssl
import subprocess
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from gstack_port_for_codex.registry import capability_source_commit, skill_source_commit


SHARED_UPSTREAM_FILES = {
    "ARCHITECTURE.md",
    "BROWSER.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "README.md",
    "SKILL.md",
    "SKILL.md.tmpl",
    "VERSION",
}
SHARED_UPSTREAM_PREFIXES = (".github/", "bin/", "scripts/", "test/")


class UpstreamDriftError(RuntimeError):
    pass


def _is_ssl_cert_failure(error: BaseException) -> bool:
    if isinstance(error, ssl.SSLCertVerificationError):
        return True
    if isinstance(error, ssl.SSLError) and "CERTIFICATE_VERIFY_FAILED" in str(error):
        return True
    return False


def fetch_json_with_curl(url: str, token: str | None = None) -> dict[str, Any]:
    if not shutil.which("curl"):
        raise UpstreamDriftError("curl is not available for SSL fallback.")

    command = [
        "curl",
        "-fsSL",
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        "User-Agent: gstack-port-for-codex-upstream-drift",
    ]
    if token:
        command.extend(("-H", f"Authorization: Bearer {token}"))
    command.append(url)

    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip()
        raise UpstreamDriftError(f"GitHub API request via curl failed: {detail}") from exc

    return json.loads(completed.stdout)


def parse_github_repo(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if parsed.netloc != "github.com":
        raise ValueError(f"Unsupported upstream host in repo URL: {url!r}")

    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]

    parts = path.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError(f"Could not parse owner/repo from URL: {url!r}")

    return parts[0], parts[1]


def fetch_json(url: str, token: str | None = None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "gstack-port-for-codex-upstream-drift",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)

    try:
        with urlopen(request) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        raise UpstreamDriftError(f"GitHub API request failed with HTTP {exc.code}: {detail}") from exc
    except ssl.SSLError as exc:
        if _is_ssl_cert_failure(exc):
            return fetch_json_with_curl(url, token=token)
        raise UpstreamDriftError(f"GitHub API request failed: {exc}") from exc
    except URLError as exc:
        if isinstance(exc.reason, BaseException) and _is_ssl_cert_failure(exc.reason):
            return fetch_json_with_curl(url, token=token)
        raise UpstreamDriftError(f"GitHub API request failed: {exc.reason}") from exc


def fetch_repo_metadata(owner: str, repo: str, token: str | None = None) -> dict[str, Any]:
    return fetch_json(f"https://api.github.com/repos/{owner}/{repo}", token=token)


def fetch_branch_head(owner: str, repo: str, branch: str, token: str | None = None) -> dict[str, Any]:
    return fetch_json(f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}", token=token)


def fetch_compare(owner: str, repo: str, base: str, head: str, token: str | None = None) -> dict[str, Any]:
    return fetch_json(
        f"https://api.github.com/repos/{owner}/{repo}/compare/{base}...{head}",
        token=token,
    )


def classify_changed_paths(
    changed_paths: list[str],
    skill_map: dict[str, Any],
) -> dict[str, Any]:
    entries = _map_entries(skill_map)
    skill_paths = {_entry_id(entry): [] for entry in entries}
    shared_paths: list[str] = []
    unmatched_paths: list[str] = []

    for path in changed_paths:
        matched_slug: str | None = None
        for entry in entries:
            slug = _entry_id(entry)
            if _path_matches_entry(path, entry):
                matched_slug = slug
                skill_paths[slug].append(path)
                break

        if matched_slug:
            continue

        if path in SHARED_UPSTREAM_FILES or path.startswith(SHARED_UPSTREAM_PREFIXES):
            shared_paths.append(path)
        else:
            unmatched_paths.append(path)

    return {
        "skills": {slug: sorted(paths) for slug, paths in skill_paths.items() if paths},
        "shared": sorted(shared_paths),
        "unmatched": sorted(unmatched_paths),
    }


def _map_entries(upstream_map: dict[str, Any]) -> list[dict[str, Any]]:
    if "capabilities" in upstream_map:
        return upstream_map["capabilities"]
    return upstream_map["skills"]


def _entry_id(entry: dict[str, Any]) -> str:
    return str(entry.get("id") or entry["upstream_slug"])


def _entry_source_commit(upstream_map: dict[str, Any], entry: dict[str, Any]) -> str:
    if "capabilities" in upstream_map:
        return capability_source_commit(upstream_map, entry)
    return skill_source_commit(upstream_map, entry)


def _path_matches_entry(path: str, entry: dict[str, Any]) -> bool:
    explicit_paths = entry.get("upstream_paths")
    if explicit_paths:
        for configured_path in explicit_paths:
            if configured_path.endswith("*") and path.startswith(configured_path[:-1]):
                return True
            if configured_path.endswith("/") and path.startswith(configured_path):
                return True
            if path == configured_path:
                return True
        return False

    slug = entry["upstream_slug"]
    return path.startswith(f"{slug}/") or path.startswith(f"skills/{slug}/")


def classify_skill_changes_by_source(
    skill_map: dict[str, Any],
    compares_by_source: dict[str, dict[str, Any]],
) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Return skill-local changes using each skill's own port source commit.

    The map-level baseline remains useful for reporting broad upstream runtime
    drift. It is not, however, a truthful freshness boundary for skills that
    were refreshed from a newer upstream commit.
    """
    changes: dict[str, list[str]] = {}
    sources: dict[str, str] = {}

    for skill in _map_entries(skill_map):
        slug = _entry_id(skill)
        source_commit = _entry_source_commit(skill_map, skill)
        changed_paths = [
            file["filename"]
            for file in compares_by_source[source_commit].get("files", [])
        ]
        matched = sorted(
            path
            for path in changed_paths
            if _path_matches_entry(path, skill)
        )
        if matched:
            changes[slug] = matched
            sources[slug] = source_commit

    return changes, sources


def build_drift_report(
    skill_map: dict[str, Any],
    repo_metadata: dict[str, Any],
    branch_head: dict[str, Any],
    compare_data: dict[str, Any],
    skill_changes: dict[str, list[str]] | None = None,
    skill_change_sources: dict[str, str] | None = None,
) -> dict[str, Any]:
    changed_paths = [file["filename"] for file in compare_data.get("files", [])]
    classified = classify_changed_paths(changed_paths, skill_map)

    return {
        "repo_full_name": repo_metadata["full_name"],
        "default_branch": repo_metadata["default_branch"],
        "compare_url": compare_data["html_url"],
        "pinned_commit": skill_map["source"]["commit"],
        "latest_commit": branch_head["sha"],
        "latest_commit_url": branch_head["html_url"],
        "status": compare_data["status"],
        "ahead_by": compare_data["ahead_by"],
        "behind_by": compare_data["behind_by"],
        "total_commits": compare_data["total_commits"],
        "changed_files_count": len(changed_paths),
        "skill_changes": skill_changes if skill_changes is not None else classified["skills"],
        "skill_change_sources": skill_change_sources or {},
        "shared_changes": classified["shared"],
        "unmatched_changes": classified["unmatched"],
    }


def check_upstream_drift(skill_map: dict[str, Any], token: str | None = None) -> dict[str, Any]:
    owner, repo = parse_github_repo(skill_map["source"]["repo"])
    repo_metadata = fetch_repo_metadata(owner, repo, token=token)
    default_branch = repo_metadata["default_branch"]
    branch_head = fetch_branch_head(owner, repo, default_branch, token=token)
    compare_data = fetch_compare(
        owner,
        repo,
        skill_map["source"]["commit"],
        default_branch,
        token=token,
    )
    compares_by_source = {skill_map["source"]["commit"]: compare_data}
    for source_commit in {
        _entry_source_commit(skill_map, skill) for skill in _map_entries(skill_map)
    }:
        if source_commit not in compares_by_source:
            compares_by_source[source_commit] = fetch_compare(
                owner,
                repo,
                source_commit,
                default_branch,
                token=token,
            )

    skill_changes, skill_change_sources = classify_skill_changes_by_source(
        skill_map,
        compares_by_source,
    )
    return build_drift_report(
        skill_map,
        repo_metadata,
        branch_head,
        compare_data,
        skill_changes=skill_changes,
        skill_change_sources=skill_change_sources,
    )


def _summarize_paths(paths: list[str], limit: int = 3) -> list[str]:
    if len(paths) <= limit:
        return paths
    hidden_count = len(paths) - limit
    return [*paths[:limit], f"... (+{hidden_count} more)"]


def format_drift_report(report: dict[str, Any]) -> str:
    lines = [
        f"Upstream repo: {report['repo_full_name']}",
        f"Pinned commit: {report['pinned_commit']}",
        f"Default branch: {report['default_branch']}",
        f"Latest commit: {report['latest_commit']}",
        f"Latest commit URL: {report['latest_commit_url']}",
        f"Compare URL: {report['compare_url']}",
    ]

    if report["ahead_by"] == 0 and report["changed_files_count"] == 0:
        lines.append("")
        lines.append("No upstream drift detected.")
        return "\n".join(lines)

    lines.extend(
        (
            "",
            f"Commits since pin: {report['ahead_by']}",
            f"Changed files since pin: {report['changed_files_count']}",
        )
    )

    if report["skill_changes"]:
        lines.append("")
        lines.append("Impacted upstream items:")
        for slug, paths in report["skill_changes"].items():
            source_commit = report.get("skill_change_sources", {}).get(slug)
            source_suffix = f" since {source_commit[:7]}" if source_commit else ""
            lines.append(f"- {slug} ({len(paths)} files{source_suffix})")
            for path in _summarize_paths(paths):
                lines.append(f"  - {path}")

    if report["shared_changes"]:
        lines.append("")
        lines.append("Shared upstream paths:")
        for path in _summarize_paths(report["shared_changes"], limit=8):
            lines.append(f"- {path}")

    if report["unmatched_changes"]:
        lines.append("")
        lines.append("Unmatched upstream paths:")
        for path in _summarize_paths(report["unmatched_changes"], limit=8):
            lines.append(f"- {path}")

    return "\n".join(lines)


def report_as_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True)


def github_token_from_env() -> str | None:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    if not shutil.which("gh"):
        return None

    completed = subprocess.run(
        ["gh", "auth", "token"],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout.strip() or None if completed.returncode == 0 else None
