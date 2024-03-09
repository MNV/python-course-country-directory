"""
Тестирование функций сбора информации о погоде.
"""

import pytest

from collectors.collector import WeatherCollector
from collectors.models import LocationDTO


@pytest.mark.asyncio
class TestClientCountry:
    """
    Тестирование клиента для получения информации о погоде.
    """

    @pytest.fixture
    def collector(self):
        return WeatherCollector()

    @pytest.fixture
    def location(self):
        return LocationDTO(
            capital="London",
            alpha2code="uk",
        )

    async def test_collect_weather_data(self, collector, location):
        await collector.collect(frozenset([location]))

    async def test_read_weather_data(self, collector, location):
        result = await collector.read(location)

        assert result is not None
        assert result.timezone == 0
