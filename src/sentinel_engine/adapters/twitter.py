"""Twitter adapter mock implementation."""

from __future__ import annotations

from typing import Any

from sentinel_engine.adapters.base import Adapter, SearchResult, AdapterResult


class TwitterAdapter(Adapter):
    """Mock Twitter adapter for testing purposes."""

    def __init__(self, name: str = "twitter", config: dict[str, Any] | None = None) -> None:
        super().__init__(name=name, config=config)
        self._platform = "twitter"

    @property
    def platform_id(self) -> str:
        return self._platform

    async def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search Twitter for tweets matching the query."""
        self._search_count += 1
        # Return mock results based on query keywords
        results: list[SearchResult] = []
        # Simple mock: generate results based on query terms
        query_lower = query.lower()
        if "python" in query_lower:
            results.append(SearchResult(
                title="Python announcement on Twitter",
                url="https://twitter.com/example/status/1",
                snippet="Exciting Python news coming soon!",
                platform="twitter",
                metadata={"source": "mock"},
            ))
        if "ai" in query_lower:
            results.append(SearchResult(
                title="AI research breakthrough",
                url="https://twitter.com/example/status/2",
                snippet="New AI model sets state-of-the-art",
                platform="twitter",
                metadata={"source": "mock"},
            ))
        # If no specific matches, return generic results
        if not results:
            results.append(SearchResult(
                title=f"Results for: {query}",
                url="https://twitter.com/search?q=" + query.replace(" ", "+"),
                snippet=f"Mock search results for '{query}' on Twitter",
                platform="twitter",
                metadata={"source": "mock"},
            ))
        return results[:limit]

    async def fetch(self, url: str) -> SearchResult | None:
        """Fetch a specific Twitter tweet URL."""
        self._fetch_count += 1
        # Mock fetch returns basic tweet info
        return SearchResult(
            title="Mock Twitter Tweet",
            url=url,
            snippet="This is a mock tweet fetched from the adapter.",
            platform="twitter",
            metadata={"source": "mock", "url": url},
        )

    async def health_check(self) -> bool:
        """Check Twitter adapter health."""
        return True
