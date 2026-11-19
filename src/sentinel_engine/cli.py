"""Sentinel Engine - CLI entry point."""

from __future__ import annotations

import asyncio
import typer
from rich.console import Console
from rich.table import Table

from sentinel_engine.config import get_config
from sentinel_engine.channels import get_registry, SearchResult

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


@app.command()
def search(query: str, limit: int = typer.Option(10, "--limit", "-l", help="Maximum results")) -> None:
    """Search across all registered channels."""
    async def _do_search():
        registry = get_registry()
        all_results: list[SearchResult] = []
        platforms_found: list[str] = []
        
        for channel in registry.list_all():
            platform = channel.platform
            platforms_found.append(platform)
            try:
                results = await channel.search(query, limit)
                all_results.extend(results)
            except Exception as e:
                console.print("[red]Error searching {}:[/red] {}".format(platform, e))
        
        # Deduplicate by URL
        seen_urls: set[str] = set()
        unique_results = []
        for r in all_results:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                unique_results.append(r)
        
        if not unique_results:
            console.print("[yellow]No results found for query: '{}'[/yellow]".format(query))
            return
        
        table = Table(title="Search Results: {}".format(query))
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", style="cyan")
        table.add_column("Platform", style="green")
        table.add_column("URL", style="magenta")
        table.add_column("Snippet", style="white")
        
        for i, r in enumerate(unique_results[:limit], 1):
            snippet = r.snippet[:100] if r.snippet else ""
            table.add_row(str(i), r.title, r.platform, r.url, snippet)
        
        console.print(table)
        n_platforms = len(set(platforms_found))
        console.print("Found {} results across {} platforms".format(len(unique_results), n_platforms))
    
    asyncio.run(_do_search())
