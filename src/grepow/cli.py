from __future__ import annotations

import argparse
import asyncio
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path

from tqdm import tqdm

from .core import RepoFiles, clone_full, clone_sparse, fetch_hits, group_repos


__all__ = ["main"]

CloneFn = Callable[[RepoFiles, Path], Awaitable[str]]


async def clone_all(
    repos: list[RepoFiles],
    target: Path,
    clone_fn: CloneFn,
    jobs: int,
) -> None:
    """Clone repos concurrently with bounded parallelism."""
    sem = asyncio.Semaphore(jobs)
    pbar = tqdm(total=len(repos), unit="repo")

    async def task(repo: RepoFiles) -> None:
        async with sem:
            try:
                msg = await clone_fn(repo, target)
                pbar.set_postfix_str(msg)
            except RuntimeError as e:
                pbar.set_postfix_str(f"{repo.owner_repo}: FAILED")
                print(f"\n{repo.owner_repo}: {e}", file=sys.stderr)
            pbar.update()

    try:
        await asyncio.gather(*(task(r) for r in repos))
    finally:
        pbar.close()


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
    parser.add_argument("-j", "--jobs", type=int, default=8, help="Parallel clones")
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

    asyncio.run(clone_all(repos, args.target, clone_fn, args.jobs))
    return 0
