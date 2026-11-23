"""Integration tests for end-to-end search workflow (CLI -> API -> Channel -> Results)."""

from typing import Any

import pytest
from typer.testing import CliRunner

from sentinel_engine.channels import get_registry, set_registry, SearchResult, MockChannel
from sentinel_engine.cli import app as cli_app
from sentinel_engine.main import app as api_app
from httpx import ASGITransport, AsyncClient


def _make_mock_results() -> list[SearchResult]:
    """Create mock search results for testing."""
    return [
        SearchResult(
            title="Test Result 1",
            url="https://example.com/result1",
            snippet="This is a test snippet for result 1",
            platform="mock",
        ),
        SearchResult(
            title="Test Result 2",
            url="https://example.com/result2",
            snippet="This is a test snippet for result 2",
            platform="mock",
        ),
    ]


@pytest.fixture(autouse=True)
def setup_registry() -> Any:
    """Set up a fresh registry with mock channel for each test."""
    set_registry(None)  # reset
    registry = get_registry()
    mock = MockChannel(name="mock", platform="mock")
    mock.add_result(_make_mock_results()[0])
    mock.add_result(_make_mock_results()[1])
    registry.register(mock)
    yield
    set_registry(None)  # clean up


class TestCliSearch:
    """CLI search command tests (no async)."""

    def test_cli_search_command_returns_results(self) -> None:
        """CLI 'search' command queries channels and returns results."""
        runner = CliRunner()
        result = runner.invoke(cli_app, ["search", "test"])
        assert result.exit_code == 0
        assert "Test Result 1" in result.output
        assert "Test Result 2" in result.output
        assert "mock" in result.output

    def test_cli_search_no_results(self) -> None:
        """CLI 'search' command with query returning no results."""
        runner = CliRunner()
        result = runner.invoke(cli_app, ["search", "nonexistent_query_xyz"])
        assert result.exit_code == 0
        assert "No results found" in result.output


class TestApiSearch:
    """API search endpoint tests (async)."""

    @pytest.fixture(autouse=True)
    def setup_registry(self) -> Any:
        """Set up a fresh registry with mock channel for each test."""
        set_registry(None)
        registry = get_registry()
        mock = MockChannel(name="mock", platform="mock")
        mock.add_result(_make_mock_results()[0])
        mock.add_result(_make_mock_results()[1])
        registry.register(mock)
        yield
        set_registry(None)

    @pytest.mark.asyncio
    async def test_api_search_endpoint_returns_results(self) -> None:
        """API '/search' endpoint accepts query and returns aggregated results."""
        transport = ASGITransport(app=api_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/search",
                json={"query": "test", "limit": 10},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "test"
        assert len(data["results"]) > 0
        assert "mock" in data["platforms"]

    @pytest.mark.asyncio
    async def test_api_search_deduplication(self) -> None:
        """API search deduplicates results by URL."""
        transport = ASGITransport(app=api_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/search",
                json={"query": "test", "limit": 10},
            )
        assert response.status_code == 200
        data = response.json()
        urls = [r["url"] for r in data["results"]]
        assert len(urls) == len(set(urls)), "Duplicate URLs found in results"
