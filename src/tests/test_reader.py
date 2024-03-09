"""
Тестирование функций поиска (чтения) собранной информации в файлах.
"""

import pytest
from collectors.models import (
    CountryDTO,
    LocationDTO,
    LocationInfoDTO,
    CountryNewsDTO,
    WeatherInfoDTO,
)
from reader import Reader


@pytest.mark.asyncio
class TestReader:
    @pytest.fixture
    def reader(self):
        return Reader()

    @pytest.fixture
    def location(self):
        return LocationDTO(
            capital="Moscow",
            alpha2code="ru",
        )

    async def test_find_by_country(self, reader, location):
        result = await reader.find("Russia")

        assert isinstance(result, LocationInfoDTO)

        assert result.location.name == "Russian Federation"
        assert result.location.subregion == "Eastern Europe"
        assert result.location.area == 17124442
        assert len(result.location.languages) == 1
        assert result.location.population > 145934462
        assert len(result.location.currencies) == 1
        assert len(result.location.timezones) == 9
        assert result.location.alpha2code == "RU"
        assert len(result.currency_rates) == 1
        assert len(result.location.alt_spellings) == 5

        assert result.location.capital == "Moscow"
        assert result.location.capital_longitude == 100.0
        assert result.location.capital_latitude == 60.0

        assert isinstance(result.weather, WeatherInfoDTO)
        assert result.weather.timezone == 10800

    async def test_find_by_capital(self, reader, location):
        result = await reader.find("Moscow")

        assert isinstance(result, LocationInfoDTO)

        assert result.location.name == "Russian Federation"
        assert result.location.subregion == "Eastern Europe"
        assert result.location.area == 17124442
        assert len(result.location.languages) == 1
        assert result.location.population > 145934462
        assert len(result.location.currencies) == 1
        assert len(result.location.timezones) == 9
        assert result.location.alpha2code == "RU"
        assert len(result.currency_rates) == 1
        assert len(result.location.alt_spellings) == 5

        assert result.location.capital == "Moscow"
        assert result.location.capital_longitude == 100.0
        assert result.location.capital_latitude == 60.0

        assert isinstance(result.weather, WeatherInfoDTO)
        assert result.weather.timezone == 10800

    async def test_get_weather(self, reader, location):
        result = await reader.get_weather(location)

        assert isinstance(result, WeatherInfoDTO)
        assert result.timezone == 10800

    async def test_get_news(self, reader, location):
        result = await reader.get_news(location)

        assert len(result) == 3
        assert isinstance(result[0], CountryNewsDTO)

    async def test_find_country(self, reader):
        result = await reader.find_country("Russia")

        assert isinstance(result, CountryDTO)
        assert result.name == "Russian Federation"
        assert result.capital == "Moscow"
