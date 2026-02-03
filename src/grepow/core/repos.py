from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from urllib.parse import quote_plus

import httpx

__all__ = ["RepoFiles", "fetch_hits", "group_repos"]


@dataclass(frozen=True, slots=True)
class RepoFiles:
    """A repository with its matched file paths."""

    owner_repo: str
    paths: frozenset[str]

    @property
    def clone_url(self) -> str:
        return f"https://github.com/{self.owner_repo}.git"

    @property
    def local_name(self) -> str:
        return self.owner_repo.replace("/", "__")


def _extract_field(hit: dict, key: str) -> str | None:
    """Extract field that may be str or {raw: str}."""
    val = hit.get(key)
    if val is None:
        return None
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return val.get("raw")
    return None


def fetch_hits(query: str, *, max_pages: int = 10) -> dict[str, set[str]]:
    """Query grep.app, return {repo: {paths...}}."""
    repo_paths: defaultdict[str, set[str]] = defaultdict(set)

    with httpx.Client(timeout=30) as client:
        for page in range(1, max_pages + 1):
            url = f"https://grep.app/api/search?q={quote_plus(query)}&page={page}"
            resp = client.get(url)
            resp.raise_for_status()
            data: dict = resp.json()

            hits: list[dict] = data.get("hits", {}).get("hits", [])
            if not hits:
                break

            for hit in hits:
                repo = _extract_field(hit, "repo")
                path = _extract_field(hit, "path")
                if repo and path:
                    repo_paths[repo].add(path)

    return dict(repo_paths)


def group_repos(repo_paths: dict[str, set[str]]) -> list[RepoFiles]:
    """Convert raw dict to typed list."""
    return [RepoFiles(repo, frozenset(paths)) for repo, paths in repo_paths.items()]
