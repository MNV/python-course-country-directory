"""
Тестирование функций генерации выходных данных.
"""
import datetime

import pytest
from collectors.models import (
    CountryDTO,
    CurrencyInfoDTO,
    LanguagesInfoDTO,
    LocationInfoDTO,
    NewsInfoDTO,
    WeatherInfoDTO,
    CoordInfoDTO,
)
from renderer import Renderer


class TestRenderer:
    location = LocationInfoDTO(
        location=CountryDTO(
            alpha2code="RU",
            capital="Moscow",
            currencies={CurrencyInfoDTO(code="USD")},
            languages={LanguagesInfoDTO(name="Russian", native_name="Русский")},
            flag="test",
            subregion="test",
            name="Russia",
            population=3,
            area=3,
            longitude=3,
            latitude=3,
            alt_spellings=["test"],
            timezones=[3],
        ),
        weather=WeatherInfoDTO(
            coord=CoordInfoDTO(
                lon=-0.1257,
                lat=51.5085,
            ),
            temp=13.92,
            pressure=1023,
            humidity=54,
            wind_speed=4.63,
            description="scattered clouds",
            visibility=2500,
            timezone=0,
        ),
        currency_rates={"USD": 1.0},
        news=[
            NewsInfoDTO(
                source="test",
                published_at="test",
                title="test",
                description="test",
                url="test",
                url_to_image="test",
            )
        ],
    )

    @pytest.mark.asyncio
    async def test_render(self):
        renderer = Renderer(self.location)
        results = await renderer.render()
        assert len(results) == 24
        first_column = [
            "",
            "Страна",
            "Столица",
            "Площадь",
            "Регион",
            "Координатыстолицы",
            "Языки",
            "Населениестраны",
            "Курсывалют",
            "",
            "Часовойпояс",
            "Текущеевремя",
            "",
            "Температура",
            "Описаниепогоды",
            "Видемость",
            "Скоростьветра",
            "",
            "Источник",
            "Автор",
            "Заголовок",
            "Описание",
            "Ссылка",
            "Датапубликации",
        ]
        second_column = [
            None,
            "Russia",
            "Moscow",
            "3.0",
            "test",
            "51°30’30.60”N,0°7’32.52”W",
            "Russian(Русский)",
            "3чел.",
            "USD=1.00руб.",
            None,
            "UTC+00:00",
            datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M").replace(" ", ""),
            None,
            "13.92°C",
            "scatteredclouds",
            "2500м.",
            "4.63м/с",
            None,
            "test",
            "Нетданных",
            "test",
            "test",
            "test",
        ]
        for result, first_col, second_col in zip(results, first_column, second_column):
            if "-" in result:
                continue
            result = result.replace(" ", "").split("|")
            assert result[1] == first_col, f"{result[1]} != {first_col}"
            assert result[2] == second_col, f"{result[2]} != {second_col}"

    @pytest.mark.asyncio
    async def test_format_languages(self):
        renderer = Renderer(self.location)
        result = await renderer._format_languages()
        assert result == "Russian (Русский)"

    @pytest.mark.asyncio
    async def test_format_currencies_rates(self):
        renderer = Renderer(self.location)
        result = await renderer._format_currency_rates()
        assert result == "USD = 1.00 руб."

    @pytest.mark.asyncio
    async def test_format_population(self):
        renderer = Renderer(self.location)
        result = await renderer._format_population()
        assert result == "3"
