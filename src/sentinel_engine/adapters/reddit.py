"""Reddit adapter mock implementation."""

from __future__ import annotations

from typing import Any

from sentinel_engine.adapters.base import Adapter, SearchResult


class RedditAdapter(Adapter):
    """Mock Reddit adapter for testing purposes."""

    def __init__(self, name: str = "reddit", config: dict[str, Any] | None = None) -> None:
        super().__init__(name=name, config=config)
        self._platform = "reddit"

    @property
    def platform_id(self) -> str:
        return self._platform

    async def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search Reddit for posts matching the query."""
        self._search_count += 1
        # Return mock results based on query keywords
        results: list[SearchResult] = []
        query_lower = query.lower()
        if "programming" in query_lower or "code" in query_lower:
            results.append(SearchResult(
                title="Programming discussion on Reddit",
                url="https://reddit.com/r/programming/example",
                snippet="Discussion about recent programming trends and best practices.",
                platform="reddit",
                metadata={"subreddit": "programming"},
            ))
        if "python" in query_lower:
            results.append(SearchResult(
                title="Python subreddit post",
                url="https://reddit.com/r/Python/example",
                snippet="Latest Python package releases and updates.",
                platform="reddit",
                metadata={"subreddit": "Python"},
            ))
        if not results:
            results.append(SearchResult(
                title=f"Reddit search results for: {query}",
                url="https://www.reddit.com/search?q=" + query.replace(" ", "+"),
                snippet=f"Mock Reddit search results for '{query}'",
                platform="reddit",
                metadata={"source": "mock"},
            ))
        return results[:limit]

    async def fetch(self, url: str) -> SearchResult | None:
        """Fetch a specific Reddit post URL."""
        self._fetch_count += 1
        return SearchResult(
            title="Mock Reddit Post",
            url=url,
            snippet="This is a mock Reddit post fetched from the adapter.",
            platform="reddit",
            metadata={"source": "mock", "url": url},
        )

    async def health_check(self) -> bool:
        """Check Reddit adapter health."""
        return True
