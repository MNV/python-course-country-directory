"""
Тестирование функций генерации выходных данных.
"""

import pytest

from collectors.models import (
    CountryDTO,
    CurrencyInfoDTO,
    LanguagesInfoDTO,
    LocationInfoDTO,
    WeatherInfoDTO,
    CountryNewsDTO,
)
from renderer import Renderer


@pytest.mark.asyncio
class TestRenderer:
    location = LocationInfoDTO(
        location=CountryDTO(
            capital="Moscow",
            capital_latitude=25,
            capital_longitude=50,
            alpha2code="RU",
            alt_spellings=["Россия"],
            currencies={CurrencyInfoDTO(code="RUB")},
            flag="x",
            languages={LanguagesInfoDTO(name="Russian", native_name="Русский")},
            name="Russia",
            population=146000000,
            subregion="europe",
            timezones=[1, 10800, 3, 4],
            area=100000000,
        ),
        weather=WeatherInfoDTO(
            timezone=10800,
            temp=27,
            pressure=842,
            humidity=35,
            wind_speed=7,
            visibility=120,
            dt=1709996768,
            description="sunny",
        ),
        currency_rates={"USD": 95.0},
        news=[
            CountryNewsDTO(
                title="title1",
                description="desc1",
                url="url1",
                published_at="2024-03-09T14:14:00Z",
            )
        ],
    )

    @pytest.fixture
    def renderer(self):
        return Renderer(self.location)

    async def test_render_count_row(self, renderer):
        result = await renderer.render()

        assert len(result) == 36

    async def test_render_format_languages(self, renderer):
        result = await renderer.render()

        assert "Russian (Русский)" in result[9]

    async def test_render_format_population(self, renderer):
        result = await renderer.render()

        assert "146.000.000 чел." in result[11]

    async def test_render_format_currency_rates(self, renderer):
        result = await renderer.render()

        assert "95.0" in result[13]

    async def test_render_format_timezone(self, renderer):
        result = await renderer.render()

        assert "UTC+3" in result[31]

    async def test_render_format_news(self, renderer):
        result = await renderer.render()

        assert len(result) == 36
        assert result[35].startswith("\n\nНовости по данной стране\n")
