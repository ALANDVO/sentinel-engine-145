"""Sentinel Engine - Configuration module"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PlatformConfig(BaseModel):
    """Configuration for a single platform."""

    enabled: bool = True
    api_key: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class Config(BaseSettings):
    """Main configuration for Sentinel Engine."""

    model_config = SettingsConfigDict(
        env_prefix="SENTINEL_",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    # Platform configurations
    twitter: PlatformConfig = Field(default_factory=PlatformConfig)
    reddit: PlatformConfig = Field(default_factory=PlatformConfig)
    youtube: PlatformConfig = Field(default_factory=PlatformConfig)
    github: PlatformConfig = Field(default_factory=PlatformConfig)
    bilibili: PlatformConfig = Field(default_factory=PlatformConfig)
    xiaohongshu: PlatformConfig = Field(default_factory=PlatformConfig)

    # General settings
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".cache" / "sentinel-engine")
    log_level: str = "INFO"
    timeout: int = 30
    max_retries: int = 3

    @classmethod
    def load(cls, config_path: Path | None = None) -> Config:
        """Load configuration from file and environment."""
        data: dict[str, Any] = {}

        if config_path and config_path.exists():
            with config_path.open("r", encoding="utf-8") as f:
                file_data = yaml.safe_load(f) or {}
                data.update(file_data)

        # Environment variables take precedence via pydantic-settings
        return cls(**data)

    def save(self, config_path: Path) -> None:
        """Save configuration to YAML file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # Only save non-default values
        data = self.model_dump(exclude_defaults=True, exclude_none=True)
        with config_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    def get_platform(self, name: str) -> PlatformConfig:
        """Get platform configuration by name."""
        return getattr(self, name.lower(), PlatformConfig())


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "sentinel-engine" / "config.yaml"


def get_config(config_path: Path | None = None) -> Config:
    """Get the global configuration instance."""
    return Config.load(config_path or DEFAULT_CONFIG_PATH)
