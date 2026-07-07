"""
Thin wrapper around the public GitHub REST API used to show recent
repositories on the portfolio without hardcoding them in Angular.
Results are cached in-process for a few minutes to stay well under
GitHub's unauthenticated rate limit.
"""
from __future__ import annotations

import time

import requests
from django.conf import settings

_cache: dict = {"data": None, "expires_at": 0}
CACHE_SECONDS = 300


def get_recent_repositories(limit: int = 6) -> list[dict]:
    now = time.time()
    if _cache["data"] is not None and _cache["expires_at"] > now:
        return _cache["data"]

    headers = {"Accept": "application/vnd.github+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    url = f"https://api.github.com/users/{settings.GITHUB_USERNAME}/repos"
    try:
        resp = requests.get(
            url,
            params={"sort": "updated", "per_page": limit},
            headers=headers,
            timeout=5,
        )
        resp.raise_for_status()
        repos = [
            {
                "name": repo["name"],
                "description": repo.get("description"),
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "language": repo.get("language"),
                "updated_at": repo["updated_at"],
            }
            for repo in resp.json()
        ]
    except requests.RequestException:
        repos = []

    _cache["data"] = repos
    _cache["expires_at"] = now + CACHE_SECONDS
    return repos
