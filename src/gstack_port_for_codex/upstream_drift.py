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
    skill_paths = {
        skill["upstream_slug"]: []
        for skill in skill_map["skills"]
    }
    shared_paths: list[str] = []
    unmatched_paths: list[str] = []

    for path in changed_paths:
        matched_slug: str | None = None
        for skill in skill_map["skills"]:
            slug = skill["upstream_slug"]
            if path.startswith(f"{slug}/"):
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


def build_drift_report(
    skill_map: dict[str, Any],
    repo_metadata: dict[str, Any],
    branch_head: dict[str, Any],
    compare_data: dict[str, Any],
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
        "skill_changes": classified["skills"],
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
    return build_drift_report(skill_map, repo_metadata, branch_head, compare_data)


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
        lines.append("Impacted skill paths:")
        for slug, paths in report["skill_changes"].items():
            lines.append(f"- {slug} ({len(paths)} files)")
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
    return os.environ.get("GITHUB_TOKEN")
