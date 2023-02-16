"""
Тестирование функций поиска (чтения) собранной информации в файлах.
"""
import pytest

from collectors.models import (
    CountryDTO,
    LocationDTO,
    LocationInfoDTO,
    NewsInfoDTO,
    WeatherInfoDTO,
)
from reader import Reader


class TestReader:
    location = LocationDTO(
        alpha2code="RU",
        capital="Moscow",
    )

    @pytest.fixture
    def reader(self):
        return Reader()

    @pytest.mark.asyncio
    async def test_find(self, reader):
        location = await reader.find("Moscow")
        assert type(location) == LocationInfoDTO
        assert location.location.name == "Russian Federation"
        assert location.location.capital == "Moscow"
        assert location.location.alpha2code == "RU"
        assert len(location.location.currencies) == 1
        assert len(location.location.languages) == 1
        assert len(location.location.timezones) == 9
        assert location.location.population == 146599183
        assert location.location.area == 17124442
        assert location.weather.coord.lon == 37.6156
        assert location.weather.coord.lat == 55.7522
        assert len(location.location.alt_spellings) == 5
        assert location.location.subregion == "Eastern Europe"
        assert type(location.weather) == WeatherInfoDTO
        assert location.weather.timezone == 10800
        assert len(location.news) == 20
        assert len(location.currency_rates) == 1

    @pytest.mark.asyncio
    async def test_find_not_found(self, reader):
        location = await reader.find("test")
        assert location is None

    @pytest.mark.asyncio
    async def test_get_weather(self, reader):
        weather = await reader.get_weather(self.location)
        assert type(weather) == WeatherInfoDTO
        assert weather.timezone == 10800
        assert weather.coord.lon == 37.6156
        assert weather.coord.lat == 55.7522

    @pytest.mark.asyncio
    async def test_get_news(self, reader):
        news = await reader.get_news(self.location)
        assert len(news) == 20
        assert type(news[0]) == NewsInfoDTO

    @pytest.mark.asyncio
    async def test_find_country(self, reader):
        country = await reader.find_country("Russia")
        assert type(country) == CountryDTO
        assert country.name == "Russian Federation"
        assert country.capital == "Moscow"

    @pytest.mark.asyncio
    async def test_find_country_none(self, reader):
        country = await reader.find_country("test")
        assert country is None
