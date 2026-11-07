"""Tests for CLI commands."""

from sentinel_engine.cli import app
from typer.testing import CliRunner


def test_version_command() -> None:
    """Test version command outputs version."""
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_config_show_command() -> None:
    """Test config-show command runs without error."""
    runner = CliRunner()
    result = runner.invoke(app, ["config-show"])
    assert result.exit_code == 0
    assert "Sentinel Engine Configuration" in result.output
    assert "Cache directory" in result.output
    assert "Log level" in result.output


def test_help_command() -> None:
    """Test help command shows usage."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AI agent internet access toolkit" in result.output
