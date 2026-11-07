"""Sentinel Engine - FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    version: str


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

