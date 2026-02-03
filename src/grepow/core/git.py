from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .repos import RepoFiles

__all__ = ["run_git", "clone_sparse", "clone_full"]


def run_git(*args: str, cwd: Path | None = None) -> None:
    """Run git command, raise on failure."""
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def clone_sparse(repo: RepoFiles, target: Path) -> None:
    """Sparse-checkout repo with only matched files."""
    dest = target / repo.local_name

    if dest.exists():
        print(f"  skip (exists): {dest}")
        return

    # Clone with blob filter + sparse mode
    run_git(
        "clone",
        "--filter=blob:none",
        "--sparse",
        "--depth=1",
        repo.clone_url,
        str(dest),
    )

    # Set sparse-checkout to exactly the matched paths (no-cone for file-level)
    run_git("-C", str(dest), "sparse-checkout", "set", "--no-cone", *repo.paths)

    print(f"  cloned: {dest} ({len(repo.paths)} files)")


def clone_full(repo: RepoFiles, target: Path) -> None:
    """Full shallow clone."""
    dest = target / repo.local_name

    if dest.exists():
        print(f"  skip (exists): {dest}")
        return

    run_git("clone", "--depth=1", repo.clone_url, str(dest))
    print(f"  cloned: {dest} (full)")
