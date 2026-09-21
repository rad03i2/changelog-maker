"""Command-line interface for changelog-maker."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
from .core import parse_commit, render


def git_history(repo: Path, since: str | None, until: str | None, max_count: int) -> list[tuple[str, str]]:
    cmd = ["git", "-C", str(repo), "log", f"--max-count={max_count}", "--pretty=format:%H%x09%s"]
    if since:
        cmd.append(f"{since}..{until or 'HEAD'}")
    elif until:
        cmd.append(until)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    except FileNotFoundError as exc:
        raise RuntimeError("git executable was not found") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(exc.stderr.strip() or "unable to read git history") from exc
    rows = []
    for line in result.stdout.splitlines():
        if "\t" in line:
            rows.append(tuple(line.split("\t", 1)))
    return rows


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a Markdown changelog from Git commit history.")
    p.add_argument("repo", nargs="?", default=".", help="Git repository path (default: current directory)")
    p.add_argument("--since", help="Start after this tag/commit (for example v1.0.0)")
    p.add_argument("--until", help="End at this tag/commit (default: HEAD)")
    p.add_argument("--version", default="Unreleased", help="Version heading")
    p.add_argument("--date", dest="released", help="Release date (YYYY-MM-DD)")
    p.add_argument("--max-count", type=int, default=500, help="Maximum commits to inspect (1-10000)")
    p.add_argument("--exclude-other", action="store_true", help="Hide non-Conventional commits")
    p.add_argument("--repo-url", help="Repository URL; enables commit links")
    p.add_argument("-o", "--output", help="Write to a file instead of stdout")
    p.add_argument("--force", action="store_true", help="Allow replacing an existing output file")
    p.add_argument("--version-info", action="version", version="changelog-maker 1.0.0 — Radwan Abdulhadi Ahmed (@rad03i2)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not 1 <= args.max_count <= 10000:
        print("error: --max-count must be between 1 and 10000", file=sys.stderr); return 2
    repo = Path(args.repo).expanduser().resolve()
    if not (repo / ".git").exists():
        print(f"error: not a Git repository: {repo}", file=sys.stderr); return 2
    try:
        rows = git_history(repo, args.since, args.until, args.max_count)
        text = render([parse_commit(sha, subject) for sha, subject in rows], args.version, args.released,
                      not args.exclude_other, bool(args.repo_url), args.repo_url)
    except (RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2
    if args.output:
        target = Path(args.output)
        if target.exists() and not args.force:
            print(f"error: output exists: {target} (use --force to replace)", file=sys.stderr); return 2
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(target)
    else:
        sys.stdout.write(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
