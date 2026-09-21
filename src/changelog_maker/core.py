"""Core changelog parsing and rendering."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re

_PATTERN = re.compile(r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s+(?P<subject>.+)$")
SECTIONS = {
    "feat": "Added",
    "fix": "Fixed",
    "perf": "Performance",
    "refactor": "Changed",
    "docs": "Documentation",
    "test": "Tests",
    "build": "Build",
    "ci": "CI",
    "chore": "Maintenance",
    "revert": "Reverted",
}

@dataclass(frozen=True)
class Commit:
    sha: str
    subject: str
    type: str = "other"
    scope: str | None = None
    breaking: bool = False


def parse_commit(sha: str, subject: str) -> Commit:
    subject = subject.strip()
    match = _PATTERN.match(subject)
    if not match:
        return Commit(sha=sha[:12], subject=subject)
    data = match.groupdict()
    return Commit(
        sha=sha[:12], subject=data["subject"].strip(), type=data["type"].lower(),
        scope=data["scope"], breaking=bool(data["breaking"]),
    )


def render(commits: list[Commit], version: str = "Unreleased", released: str | None = None,
           include_other: bool = True, links: bool = False, repo_url: str | None = None) -> str:
    if links and not repo_url:
        raise ValueError("repo_url is required when links are enabled")
    groups: dict[str, list[Commit]] = {}
    breaking: list[Commit] = []
    for commit in commits:
        if commit.breaking:
            breaking.append(commit)
        section = SECTIONS.get(commit.type)
        if section is None:
            if not include_other:
                continue
            section = "Other"
        groups.setdefault(section, []).append(commit)
    stamp = released or (date.today().isoformat() if version != "Unreleased" else "")
    title = f"## [{version}]" + (f" - {stamp}" if stamp else "")
    lines = [title, ""]
    if breaking:
        lines += ["### Breaking Changes", ""] + [_bullet(c, links, repo_url) for c in breaking] + [""]
    order = list(dict.fromkeys(SECTIONS.values())) + ["Other"]
    for section in order:
        items = groups.get(section)
        if not items:
            continue
        lines += [f"### {section}", ""] + [_bullet(c, links, repo_url) for c in items] + [""]
    if len(lines) == 2:
        lines += ["_No changes._", ""]
    return "\n".join(lines).rstrip() + "\n"


def _bullet(commit: Commit, links: bool, repo_url: str | None) -> str:
    scope = f"**{commit.scope}:** " if commit.scope else ""
    sha = f"[{commit.sha[:7]}]({repo_url.rstrip('/')}/commit/{commit.sha})" if links and repo_url else f"`{commit.sha[:7]}`"
    return f"- {scope}{commit.subject} ({sha})"
