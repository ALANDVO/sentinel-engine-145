"""Tests for health endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from sentinel_engine.main import app

OK = 200


@pytest.mark.asyncio
async def test_health_endpoint() -> None:
    """Test /health endpoint returns ok status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_root_endpoint() -> None:
    """Test / endpoint returns name and version."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == OK
    data = response.json()
    assert data["name"] == "Sentinel Engine"
    assert data["version"] == "0.1.0"
