"""
Тестирование функций генерации выходных данных.
"""

import pytest
from collectors.models import (
    CountryDTO,
    CurrencyInfoDTO,
    LanguagesInfoDTO,
    LocationInfoDTO,
    CapitalDTO,
    WeatherInfoDTO,
)
from renderer import Renderer


class TestRenderer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.location = LocationInfoDTO(
            location=CountryDTO(
                name="Russian Federation",
                capital="Moscow",
                alpha2code="RU",
                alt_spellings=["Russia"],
                subregion="Eastern Europe",
                population=146599183,
                area=17124442.0,
                longitude=100,
                latitude=60,
                currencies={CurrencyInfoDTO(code="RUB")},
                languages={LanguagesInfoDTO(name="Russian", native_name="Русский")},
                flag="no",
                timezones=["UTC +9"],
            ),
            capital=CapitalDTO(
                name="Moscow",
                latitude=55.75,
                longitude=37.62,
                timezone="Europe/Moscow",
                current_time="22:14:18 on Thursday, February 16, 2023",
            ),
            weather=WeatherInfoDTO(
                description="overcast clouds",
                temp=-7.05,
                pressure=960,
                humidity=95,
                wind_speed=2.03,
                visibility=70,
            ),
            currency_rates={"USD": 71.0},
        )
        self.renderer = Renderer(self.location)

    @pytest.mark.asyncio
    async def test_render_country(self):
        table = await self.renderer.render_country()
        assert table.field_names == [
            "Страна",
            "Регион",
            "Площадь (кв. м.)",
            "Языки",
            "Население страны (чел.)",
            "Курсы валют",
        ]
        assert len(table.rows) == 1
        row = table.rows[0]
        assert self.location.location.name == row[0]
        assert self.location.location.subregion == row[1]
        assert self.location.location.area == row[2]
        assert await self.renderer._format_languages() == row[3]
        assert await self.renderer._format_population() == row[4]
        assert await self.renderer._format_currency_rates() == row[5]

    @pytest.mark.asyncio
    async def test_render_capital(self):
        table = await self.renderer.render_capital()
        assert table.field_names == [
            "Название столицы",
            "Широта",
            "Долгота",
            "Часовой пояс",
            "Текущее местное время",
        ]
        assert len(table.rows) == 1
        row = table.rows[0]
        assert self.location.capital.name == row[0]
        assert self.location.capital.latitude == row[1]
        assert self.location.capital.longitude == row[2]
        assert self.location.capital.timezone == row[3]
        assert self.location.capital.current_time == row[4]

    @pytest.mark.asyncio
    async def test_render_weather(self):
        table = await self.renderer.render_weather()
        assert table.field_names == [
            "Описание",
            "Температура (°C)",
            "Видимость (м)",
            "Скорость ветра (м/с)",
        ]
        assert len(table.rows) == 1
        row = table.rows[0]
        assert self.location.weather.description == row[0]
        assert self.location.weather.temp == row[1]
        assert self.location.weather.visibility == row[2]
        assert self.location.weather.wind_speed == row[3]
