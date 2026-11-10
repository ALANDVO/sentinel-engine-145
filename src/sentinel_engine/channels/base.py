"""Base channel classes for Sentinel Engine."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SearchResult:
    """Result from a channel search."""
    title: str
    url: str
    snippet: str
    platform: str
    metadata: dict[str, Any] | None = None


class ChannelError(Exception):
    """Base exception for channel errors."""


class Channel(ABC):
    """Abstract base class for all channels."""

    def __init__(self, name: str, config: dict[str, Any] | None = None) -> None:
        self.name = name
        self.config = config or {}

    @property
    @abstractmethod
    def platform(self) -> str:
        """Platform identifier (e.g., 'twitter', 'reddit')."""

    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """Search the channel for content matching the query."""

    @abstractmethod
    async def fetch(self, url: str) -> SearchResult | None:
        """Fetch detailed content from a specific URL."""

    async def health_check(self) -> bool:
        """Check if the channel is healthy and accessible."""
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, platform={self.platform!r})"
