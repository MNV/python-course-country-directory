"""
Тестирование клиента для получения информации о новостях
"""

import pytest

from collectors.collector import NewsCollector
from collectors.models import LocationDTO


@pytest.mark.asyncio
class TestNewsCollector:
    """
    Тестирование клиента для получения информации о новостях.
    """

    location = LocationDTO(
        capital="Moscow",
        alpha2code="RU",
    )

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.collector = NewsCollector()

    @pytest.mark.asyncio
    async def test_collect_news_success(self, mocker):
        """
        Тестирование получения информации о новостях.
        """
        await self.collector.collect(frozenset([self.location]))

    async def test_read_news_success(self, mocker):
        """
        Тестирование чтения информации о новостях.
        """
        news = await self.collector.read(self.location)
        assert len(news) == 20
