"""Adapter base class and registry for platform adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from sentinel_engine.channels.base import Channel, SearchResult


@dataclass(frozen=True)
class AdapterResult:
    """Result from an adapter operation."""
    title: str
    url: str
    snippet: str
    platform: str
    metadata: dict[str, Any] | None = None


class AdapterError(Exception):
    """Base exception for adapter errors."""


class Adapter(ABC):
    """Abstract base class for platform adapters.

    Each adapter implements search and fetch for a specific platform
    (Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu).
    """

    name: str
    platform: str

    def __init__(self, name: str = "unnamed", config: dict[str, Any] | None = None) -> None:
        self.name = name
        self.config = config or {}
        self._search_count = 0
        self._fetch_count = 0

    @property
    @abstractmethod
    def platform_id(self) -> str:
        """Platform identifier string (e.g. 'twitter', 'reddit')."""

    @property
    def platform(self) -> str:
        """Convenience property returning platform_id."""
        return self.platform_id

    async def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search the platform for content matching the query."""
        self._search_count += 1
        raise NotImplementedError

    async def fetch(self, url: str) -> SearchResult | None:
        """Fetch detailed content from a specific URL."""
        self._fetch_count += 1
        raise NotImplementedError

    async def health_check(self) -> bool:
        """Check if the adapter is healthy and accessible."""
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, platform={self.platform_id!r})"


class AdapterRegistry:
    """Registry for managing platform adapters."""

    def __init__(self) -> None:
        self._adapters: dict[str, Adapter] = {}

    def register(self, adapter: Adapter) -> None:
        """Register an adapter."""
        if adapter.platform in self._adapters:
            raise AdapterError(f"Adapter {adapter.platform!r} already registered")
        self._adapters[adapter.platform] = adapter

    def unregister(self, platform: str) -> None:
        """Unregister an adapter by platform."""
        if platform not in self._adapters:
            raise AdapterError(f"Adapter {platform!r} not found")
        del self._adapters[platform]

    def get(self, platform: str) -> Adapter | None:
        """Get an adapter by platform."""
        return self._adapters.get(platform)

    def get_all(self) -> list[Adapter]:
        """Get all registered adapters."""
        return list(self._adapters.values())

    def list_names(self) -> list[str]:
        """List all registered adapter platform names."""
        return list(self._adapters.keys())

    def __contains__(self, platform: str) -> bool:
        return platform in self._adapters

    def __len__(self) -> int:
        return len(self._adapters)


# Global registry instance
_registry: AdapterRegistry | None = None


def get_registry() -> AdapterRegistry:
    """Get the global adapter registry instance."""
    global _registry
    if _registry is None:
        _registry = AdapterRegistry()
    return _registry


def set_registry(registry: AdapterRegistry) -> None:
    """Set the global adapter registry instance (for testing)."""
    global _registry
    _registry = registry
