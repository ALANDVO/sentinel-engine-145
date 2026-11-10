"""Channel module for Sentinel Engine."""

from sentinel_engine.channels.base import Channel, ChannelError, SearchResult
from sentinel_engine.channels.mock import MockChannel
from sentinel_engine.channels.registry import ChannelRegistry, get_registry, set_registry

__all__ = [
    "Channel",
    "ChannelError",
    "ChannelRegistry",
    "MockChannel",
    "SearchResult",
    "get_registry",
    "set_registry",
]
