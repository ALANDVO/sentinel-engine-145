"""Mock channel implementation for testing."""

from __future__ import annotations

from typing import Any

from sentinel_engine.channels.base import Channel, SearchResult


class MockChannel(Channel):
    """Mock channel for testing purposes."""

    def __init__(
        self,
        name: str = "mock",
        platform: str = "mock",
        config: dict[str, Any] | None = None,
        search_results: list[SearchResult] | None = None,
    ) -> None:
        super().__init__(name, config)
        self._platform = platform
        self._search_results = search_results or []
        self._fetch_map: dict[str, SearchResult] = {r.url: r for r in self._search_results}
        self._healthy = True
        self.search_call_count = 0
        self.fetch_call_count = 0
        self.health_check_call_count = 0

    @property
    def platform(self) -> str:
        return self._platform

    async def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        self.search_call_count += 1
        # Filter results by query (simple substring match)
        filtered = [
            r for r in self._search_results
            if query.lower() in r.title.lower() or query.lower() in r.snippet.lower()
        ]
        return filtered[:limit]

    async def fetch(self, url: str) -> SearchResult | None:
        self.fetch_call_count += 1
        return self._fetch_map.get(url)

    async def health_check(self) -> bool:
        self.health_check_call_count += 1
        return self._healthy

    def set_healthy(self, healthy: bool) -> None:
        """Set health status for testing."""
        self._healthy = healthy

    def add_result(self, result: SearchResult) -> None:
        """Add a search result."""
        self._search_results.append(result)
        self._fetch_map[result.url] = result

    def clear_results(self) -> None:
        """Clear all search results."""
        self._search_results.clear()
        self._fetch_map.clear()
