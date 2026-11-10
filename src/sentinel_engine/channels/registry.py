"""Channel registry for Sentinel Engine."""

from __future__ import annotations

from sentinel_engine.channels.base import Channel, ChannelError


class ChannelRegistry:
    """Registry for managing channels."""

    def __init__(self) -> None:
        self._channels: dict[str, Channel] = {}

    def register(self, channel: Channel) -> None:
        """Register a channel."""
        if channel.name in self._channels:
            raise ChannelError(f"Channel {channel.name!r} already registered")
        self._channels[channel.name] = channel

    def unregister(self, name: str) -> None:
        """Unregister a channel by name."""
        if name not in self._channels:
            raise ChannelError(f"Channel {name!r} not found")
        del self._channels[name]

    def get(self, name: str) -> Channel | None:
        """Get a channel by name."""
        return self._channels.get(name)

    def get_by_platform(self, platform: str) -> list[Channel]:
        """Get all channels for a platform."""
        return [c for c in self._channels.values() if c.platform == platform]

    def list_all(self) -> list[Channel]:
        """List all registered channels."""
        return list(self._channels.values())

    def list_names(self) -> list[str]:
        """List all registered channel names."""
        return list(self._channels.keys())

    def __contains__(self, name: str) -> bool:
        return name in self._channels

    def __len__(self) -> int:
        return len(self._channels)


# Global registry instance
_registry: ChannelRegistry | None = None


def get_registry() -> ChannelRegistry:
    """Get the global channel registry instance."""
    global _registry
    if _registry is None:
        _registry = ChannelRegistry()
    return _registry


def set_registry(registry: ChannelRegistry) -> None:
    """Set the global channel registry instance (for testing)."""
    global _registry
    _registry = registry
