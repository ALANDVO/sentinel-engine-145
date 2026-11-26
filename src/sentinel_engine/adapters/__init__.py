"""Platform adapters for Sentinel Engine."""

from sentinel_engine.adapters.base import Adapter, AdapterRegistry
from sentinel_engine.adapters.twitter import TwitterAdapter
from sentinel_engine.adapters.reddit import RedditAdapter
from sentinel_engine.adapters.youtube import YouTubeAdapter

__all__ = [
    "Adapter",
    "AdapterRegistry",
    "TwitterAdapter",
    "RedditAdapter",
    "YouTubeAdapter",
]
