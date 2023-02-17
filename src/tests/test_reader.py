"""
Тестирование функций поиска (чтения) собранной информации в файлах.
"""
import pytest

from collectors.models import (
    CountryDTO,
    LocationDTO,
    LocationInfoDTO,
    WeatherInfoDTO,
    CapitalDTO,
)
from reader import Reader


class TestReader:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.reader = Reader()
        self.location = LocationDTO(
            alpha2code="RU",
            capital="Moscow",
        )

    @pytest.mark.asyncio
    async def test_find(self):
        country = await self.reader.find_country("Moscow")
        assert type(country) == CountryDTO
        assert country.capital == "Moscow"
        assert country.alpha2code == "RU"
        assert len(country.alt_spellings) == 5
        assert len(country.currencies) == 1
        assert len(country.languages) == 1
        assert country.name == "Russian Federation"
        assert country.population == 146599183
        assert country.area == 17124442.0
        assert country.subregion == "Eastern Europe"
        assert len(country.timezones) == 9

    @pytest.mark.asyncio
    async def test_not_found_country(self):
        country = await self.reader.find_country("testcountry")
        assert country is None

    @pytest.mark.asyncio
    async def test_find_capital(self):
        capital = await self.reader.get_capital("Moscow")
        assert type(capital) == CapitalDTO
        assert capital is not None
        assert capital.name == "Moscow"
        assert round(capital.latitude, 2) == 55.75
        assert round(capital.longitude, 2) == 37.62
        assert capital.timezone == "Europe/Moscow"
        assert capital.current_time is not None

    @pytest.mark.asyncio
    async def test_not_found_capital(self):
        capital = await self.reader.get_capital("testcapital")
        assert type(capital) == CapitalDTO
        assert capital is not None
        assert capital.name == "testcapital"
        assert capital.latitude is None
        assert capital.longitude is None
        assert capital.timezone is None
        assert capital.current_time is None

    @pytest.mark.asyncio
    async def test_get_weather(self):
        weather = await self.reader.get_weather(self.location)
        assert type(weather) == WeatherInfoDTO

    @pytest.mark.asyncio
    async def test_find_location(self):
        location = await self.reader.find("Moscow")
        assert type(location) == LocationInfoDTO
        assert type(location.location) == CountryDTO
        assert type(location.capital) == CapitalDTO
        assert type(location.weather) == WeatherInfoDTO
