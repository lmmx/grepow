from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from .core import clone_full, clone_sparse, fetch_hits, group_repos

__all__ = ["main"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sparse-checkout repos from grep.app search results"
    )
    parser.add_argument("query", help="Search query for grep.app")
    parser.add_argument("target", type=Path, help="Directory to clone repos into")
    parser.add_argument(
        "--full", action="store_true", help="Full clone instead of sparse"
    )
    parser.add_argument("--max-pages", type=int, default=10, help="Max result pages")
    args = parser.parse_args(argv)

    print(f"Searching grep.app: {args.query!r}")
    repo_paths = fetch_hits(args.query, max_pages=args.max_pages)

    if not repo_paths:
        print("No results found.")
        return 0

    repos = group_repos(repo_paths)
    total_files = sum(len(r.paths) for r in repos)
    print(f"Found {total_files} files across {len(repos)} repos\n")

    args.target.mkdir(parents=True, exist_ok=True)
    clone_fn = clone_full if args.full else clone_sparse

    for repo in repos:
        print(f"{repo.owner_repo}:")
        try:
            clone_fn(repo, args.target)
        except subprocess.CalledProcessError as e:
            print(
                f"  FAILED: {e.stderr.decode().strip() if e.stderr else e}",
                file=sys.stderr,
            )

    return 0
