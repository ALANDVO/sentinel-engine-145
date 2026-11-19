"""Sentinel Engine - FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel
from sentinel_engine.channels import SearchResult


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    version: str


class SearchRequest(BaseModel):
    """Search request body."""
    query: str
    limit: int = 10


class SearchResponse(BaseModel):
    """Search response with aggregated results."""
    query: str
    results: list[SearchResult]
    platforms: list[str]


app = FastAPI(
    title="Sentinel Engine",
    description="AI agent internet access toolkit",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(version="0.1.0")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"name": "Sentinel Engine", "version": "0.1.0"}


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Search across all registered channels."""
    from sentinel_engine.channels import get_registry

    registry = get_registry()
    all_results: list[SearchResult] = []
    platforms_found: list[str] = []

    for channel in registry.list_all():
        platform = channel.platform
        platforms_found.append(platform)
        try:
            results = await channel.search(request.query, request.limit)
            all_results.extend(results)
        except Exception as e:
            # Log but continue with other channels
            pass

    # Deduplicate by URL
    seen_urls: set[str] = set()
    unique_results = []
    for r in all_results:
        if r.url not in seen_urls:
            seen_urls.add(r.url)
            unique_results.append(r)

    return SearchResponse(
        query=request.query,
        results=unique_results,
        platforms=platforms_found,
    )
