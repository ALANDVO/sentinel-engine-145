"""Tests for channel registry and mock channel."""

import pytest
from sentinel_engine.channels import (
    Channel,
    ChannelError,
    ChannelRegistry,
    MockChannel,
    SearchResult,
    get_registry,
    set_registry,
)


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_search_result_creation(self) -> None:
        result = SearchResult(
            title="Test Title",
            url="https://example.com/test",
            snippet="Test snippet",
            platform="mock",
            metadata={"key": "value"},
        )
        assert result.title == "Test Title"
        assert result.url == "https://example.com/test"
        assert result.snippet == "Test snippet"
        assert result.platform == "mock"
        assert result.metadata == {"key": "value"}

    def test_search_result_without_metadata(self) -> None:
        result = SearchResult(
            title="Test Title",
            url="https://example.com/test",
            snippet="Test snippet",
            platform="mock",
        )
        assert result.metadata is None


class TestChannelRegistry:
    """Tests for ChannelRegistry."""

    def setup_method(self) -> None:
        # Use a fresh registry for each test
        set_registry(ChannelRegistry())

    def test_register_and_get(self) -> None:
        registry = get_registry()
        channel = MockChannel(name="test", platform="test")
        registry.register(channel)
        assert registry.get("test") is channel
        assert "test" in registry

    def test_register_duplicate_raises(self) -> None:
        registry = get_registry()
        channel1 = MockChannel(name="test", platform="test")
        channel2 = MockChannel(name="test", platform="test")
        registry.register(channel1)
        with pytest.raises(ChannelError):
            registry.register(channel2)

    def test_unregister(self) -> None:
        registry = get_registry()
        channel = MockChannel(name="test", platform="test")
        registry.register(channel)
        registry.unregister("test")
        assert registry.get("test") is None
        assert "test" not in registry

    def test_unregister_missing_raises(self) -> None:
        registry = get_registry()
        with pytest.raises(ChannelError):
            registry.unregister("nonexistent")

    def test_get_by_platform(self) -> None:
        registry = get_registry()
        channel1 = MockChannel(name="test1", platform="twitter")
        channel2 = MockChannel(name="test2", platform="twitter")
        channel3 = MockChannel(name="test3", platform="reddit")
        registry.register(channel1)
        registry.register(channel2)
        registry.register(channel3)
        twitter_channels = registry.get_by_platform("twitter")
        expected_count = 2
        assert len(twitter_channels) == expected_count
        assert all(c.platform == "twitter" for c in twitter_channels)

    def test_list_all(self) -> None:
        registry = get_registry()
        channel1 = MockChannel(name="test1", platform="twitter")
        channel2 = MockChannel(name="test2", platform="reddit")
        registry.register(channel1)
        registry.register(channel2)
        all_channels = registry.list_all()
        expected_count = 2
        assert len(all_channels) == expected_count

    def test_list_names(self) -> None:
        registry = get_registry()
        channel1 = MockChannel(name="test1", platform="twitter")
        channel2 = MockChannel(name="test2", platform="reddit")
        registry.register(channel1)
        registry.register(channel2)
        names = registry.list_names()
        assert set(names) == {"test1", "test2"}

    def test_len(self) -> None:
        registry = get_registry()
        assert len(registry) == 0
        registry.register(MockChannel(name="test1", platform="twitter"))
        assert len(registry) == 1
        registry.register(MockChannel(name="test2", platform="reddit"))
        expected_count = 2
        assert len(registry) == expected_count


class TestMockChannel:
    """Tests for MockChannel."""

    @pytest.fixture
    def mock_results(self) -> list[SearchResult]:
        return [
            SearchResult(
                title="Test Result 1",
                url="https://example.com/1",
                snippet="First test result",
                platform="mock",
            ),
            SearchResult(
                title="Test Result 2",
                url="https://example.com/2",
                snippet="Second test result",
                platform="mock",
            ),
        ]

    @pytest.fixture
    def channel(self, mock_results: list[SearchResult]) -> MockChannel:
        return MockChannel(name="mock", platform="mock", search_results=mock_results)

    @pytest.mark.asyncio
    async def test_search_returns_matching_results(self, channel: MockChannel) -> None:
        results = await channel.search("test")
        expected_count = 2
        assert len(results) == expected_count

    @pytest.mark.asyncio
    async def test_search_filters_by_query(self, channel: MockChannel) -> None:
        results = await channel.search("First")
        assert len(results) == 1
        assert results[0].title == "Test Result 1"

    @pytest.mark.asyncio
    async def test_search_respects_limit(self, channel: MockChannel) -> None:
        results = await channel.search("test", limit=1)
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_search_increments_call_count(self, channel: MockChannel) -> None:
        assert channel.search_call_count == 0
        await channel.search("test")
        assert channel.search_call_count == 1
        await channel.search("test")
        expected_count = 2
        assert channel.search_call_count == expected_count

    @pytest.mark.asyncio
    async def test_fetch_returns_result_by_url(self, channel: MockChannel) -> None:
        result = await channel.fetch("https://example.com/1")
        assert result is not None
        assert result.title == "Test Result 1"

    @pytest.mark.asyncio
    async def test_fetch_returns_none_for_unknown_url(self, channel: MockChannel) -> None:
        result = await channel.fetch("https://unknown.com")
        assert result is None

    @pytest.mark.asyncio
    async def test_fetch_increments_call_count(self, channel: MockChannel) -> None:
        assert channel.fetch_call_count == 0
        await channel.fetch("https://example.com/1")
        assert channel.fetch_call_count == 1

    @pytest.mark.asyncio
    async def test_health_check_returns_healthy_by_default(self, channel: MockChannel) -> None:
        healthy = await channel.health_check()
        assert healthy is True

    @pytest.mark.asyncio
    async def test_health_check_respects_healthy_flag(self, channel: MockChannel) -> None:
        channel.set_healthy(False)
        healthy = await channel.health_check()
        assert healthy is False

    @pytest.mark.asyncio
    async def test_health_check_increments_call_count(self, channel: MockChannel) -> None:
        assert channel.health_check_call_count == 0
        await channel.health_check()
        assert channel.health_check_call_count == 1

    @pytest.mark.asyncio
    async def test_add_result(self, channel: MockChannel) -> None:
        new_result = SearchResult(
            title="New Result",
            url="https://example.com/3",
            snippet="New test result",
            platform="mock",
        )
        channel.add_result(new_result)
        results = await channel.search("New")
        assert len(results) == 1
        assert results[0].title == "New Result"

    @pytest.mark.asyncio
    async def test_clear_results(self, channel: MockChannel) -> None:
        channel.clear_results()
        results = await channel.search("test")
        assert len(results) == 0


class TestChannelBase:
    """Tests for abstract Channel base class."""

    def test_cannot_instantiate_abstract_channel(self) -> None:
        with pytest.raises(TypeError):
            Channel(name="test")  # type: ignore[abstract]

    def test_channel_repr(self) -> None:
        channel = MockChannel(name="test", platform="twitter")
        repr_str = repr(channel)
        assert "MockChannel" in repr_str
        assert "test" in repr_str
        assert "twitter" in repr_str
