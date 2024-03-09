"""
Тестирование функций сбора информации о новостях.
"""

import pytest

from collectors.collector import NewsCollector
from collectors.models import LocationDTO


@pytest.mark.asyncio
class TestClientCountry:
    """
    Тестирование клиента для получения информации о новостях.
    """

    @pytest.fixture
    def collector(self):
        return NewsCollector()

    @pytest.fixture
    def location(self):
        return LocationDTO(
            capital="Moscow",
            alpha2code="ru",
        )

    async def test_collect_news(self, collector, location):
        await collector.collect(frozenset([location]))

    async def test_read_news(self, collector, location):
        result = await collector.read(location)
        assert len(result) == 3
