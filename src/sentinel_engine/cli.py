"""Sentinel Engine - CLI entry point."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from sentinel_engine.config import get_config

app = typer.Typer(
    name="sentinel-engine",
    help="AI agent internet access toolkit",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Sentinel Engine - Give your AI agent eyes to see the entire internet."""
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")


@app.command()
def version() -> None:
    """Show version information."""
    console.print("Sentinel Engine 0.1.0")


@app.command()
def config_show() -> None:
    """Show current configuration."""
    config = get_config()
    table = Table(title="Sentinel Engine Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Cache directory", str(config.cache_dir))
    table.add_row("Log level", config.log_level)
    table.add_row("Timeout (s)", str(config.timeout))
    table.add_row("Max retries", str(config.max_retries))
    
    console.print(table)
    console.print()
    console.print("[bold]Platforms:[/bold]")
    for platform in ["twitter", "reddit", "youtube", "github", "bilibili", "xiaohongshu"]:
        pc = config.get_platform(platform)
        status = "[green]enabled[/green]" if pc.enabled else "[red]disabled[/red]"
        key_status = "set" if pc.api_key else "not set"
        console.print(f"  {platform}: {status}, API key: {key_status}")


if __name__ == "__main__":
    app()
