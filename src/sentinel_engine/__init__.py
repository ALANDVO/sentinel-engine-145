"""Sentinel Engine - AI agent internet access toolkit."""

from sentinel_engine.channels import (
    Channel,
    ChannelError,
    ChannelRegistry,
    MockChannel,
    SearchResult,
    get_registry,
)
from sentinel_engine.config import Config, PlatformConfig, get_config

__version__ = "0.1.0"
__author__ = "Alan Vo"
__email__ = "alanvo@gmail.com"

__all__ = [
    "Channel",
    "ChannelError",
    "ChannelRegistry",
    "Config",
    "MockChannel",
    "PlatformConfig",
    "SearchResult",
    "get_config",
    "get_registry",
]
