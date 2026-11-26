"""YouTube adapter mock implementation."""

from __future__ import annotations

from typing import Any

from sentinel_engine.adapters.base import Adapter, SearchResult


class YouTubeAdapter(Adapter):
    """Mock YouTube adapter for testing purposes."""

    def __init__(self, name: str = "youtube", config: dict[str, Any] | None = None) -> None:
        super().__init__(name=name, config=config)
        self._platform = "youtube"

    @property
    def platform_id(self) -> str:
        return self._platform

    async def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search YouTube for videos matching the query."""
        self._search_count += 1
        # Return mock results based on query keywords
        results: list[SearchResult] = []
        query_lower = query.lower()
        if "tutorial" in query_lower:
            results.append(SearchResult(
                title="Python Tutorial for Beginners",
                url="https://www.youtube.com/watch?v=PYTUT123",
                snippet="Learn Python from scratch in this complete tutorial course.",
                platform="youtube",
                metadata={"duration": "10:00", "views": "100K"},
            ))
        if "music" in query_lower:
            results.append(SearchResult(
                title="Best Music of 2024",
                url="https://www.youtube.com/watch?v=MUSIC456",
                snippet="Top music releases and trending songs of 2024.",
                platform="youtube",
                metadata={"duration": "1:30:00", "views": "5M"},
            ))
        if not results:
            results.append(SearchResult(
                title=f"YouTube search results for: {query}",
                url="https://www.youtube.com/results?search_query=" + query.replace(" ", "+"),
                snippet=f"Mock YouTube search results for '{query}'",
                platform="youtube",
                metadata={"source": "mock"},
            ))
        return results[:limit]

    async def fetch(self, url: str) -> SearchResult | None:
        """Fetch a specific YouTube video URL."""
        self._fetch_count += 1
        return SearchResult(
            title="Mock YouTube Video",
            url=url,
            snippet="This is a mock YouTube video fetched from the adapter.",
            platform="youtube",
            metadata={"source": "mock", "url": url},
        )

    async def health_check(self) -> bool:
        """Check YouTube adapter health."""
        return True
