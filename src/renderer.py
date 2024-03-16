"""
Функции для формирования выходной информации.
"""

import re
from datetime import timedelta
from decimal import ROUND_HALF_UP, Decimal

from tabulate import tabulate

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> tuple[str, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """

        table = [
            ["Страна:", self.location_info.location.name],
            ["Столица:", self.location_info.location.capital],
            ["Регион:", self.location_info.location.subregion],
            ["Языки:", await self._format_languages()],
            ["Население страны:", f"{await self._format_population()} чел."],
            ["Курсы валют:", await self._format_currency_rates()],
            ["Погода:", f"{self.location_info.weather.temp} °C"],
            ["Описание погоды:", self.location_info.weather.description],
            ["Скорость ветра:", self.location_info.weather.wind_speed],
            ["Видимость:", self.location_info.weather.visibility],
            ["Площадь:", f"{self.location_info.location.area} км^2"],
            [
                "Широта и долгота:",
                f"({self.location_info.location.latitude}, {self.location_info.location.longitude})",
            ],
            [
                "Местное время:",
                f"{await self._format_time()} ({self.location_info.location.timezones[0]})",
            ],
            ["Новости:", await self._format_news()],
        ]

        return tabulate(table, ["Параметр", "Значение"], tablefmt="simple").split("\n")

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )

    async def _format_time(self) -> str:
        """
        Форматирование местного времени.

        :return:
        """

        time = self.location_info.timestamp + await self._parse_tz(
            self.location_info.location.timezones[0]
        )
        return time.strftime("%H:%M:%S")

    async def _parse_tz(self, tzstr: str) -> timedelta:
        p = re.compile("UTC([+-])(\d\d):(\d\d)")
        m = p.search(tzstr)
        tz_offset = timedelta(0)
        if m:
            sign = m.group(1)
            try:
                hs = m.group(2).lstrip("0")
                ms = m.group(3).lstrip("0")
            except:
                return tz_offset

            tz_offset = timedelta(
                hours=int(hs) if hs else 0, minutes=int(ms) if ms else 0
            )

        return tz_offset

    async def _format_news(self) -> str:
        """
        Форматирование новостей.

        :return:
        """
        res = "\n"
        for (i, newsDTO) in enumerate(self.location_info.news.news):
            res += f"{i+1}) \"{newsDTO.title}\". {newsDTO.description if newsDTO.description is not None else ''}\n"

        return res
