"""
Тестирование функций сбора информации о погоде.
"""
import pytest
from collectors.collector import WeatherCollector
from collectors.models import LocationDTO


class TestCollectorWeather:
    """
    Тестирование функций сбора информации о погоде.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.collector = WeatherCollector()
        self.location = LocationDTO(
            capital="Yerevan",
            alpha2code="AM",
        )

    @pytest.mark.asyncio
    async def test_read_weather(self):
        """
        Тестирование чтения информации о погоде.
        """
        weather = await self.collector.read(self.location)
        assert weather is not None

    @pytest.mark.asyncio
    async def test_collect_weather(self):
        """
        Тестирование получения информации о погоде.
        """
        await self.collector.collect(frozenset([self.location]))
