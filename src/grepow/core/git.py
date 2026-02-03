from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .repos import RepoFiles

__all__ = ["clone_sparse", "clone_full"]


async def run_git(*args: str, cwd: Path | None = None) -> None:
    """Run git command, raise on failure."""
    proc = await asyncio.create_subprocess_exec(
        "git",
        *args,
        cwd=cwd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            stderr.decode().strip() if stderr else f"git {args[0]} failed"
        )


async def clone_sparse(repo: RepoFiles, target: Path) -> str:
    """Sparse-checkout repo with only matched files. Returns status message."""
    dest = target / repo.local_name

    if dest.exists():
        return f"{repo.owner_repo}: skip (exists)"

    await run_git(
        "clone",
        "--filter=blob:none",
        "--sparse",
        "--depth=1",
        repo.clone_url,
        str(dest),
    )
    await run_git("-C", str(dest), "sparse-checkout", "set", "--no-cone", *repo.paths)

    return f"{repo.owner_repo}: cloned ({len(repo.paths)} files)"


async def clone_full(repo: RepoFiles, target: Path) -> str:
    """Full shallow clone. Returns status message."""
    dest = target / repo.local_name

    if dest.exists():
        return f"{repo.owner_repo}: skip (exists)"

    await run_git("clone", "--depth=1", repo.clone_url, str(dest))
    return f"{repo.owner_repo}: cloned (full)"
