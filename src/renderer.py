"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from collectors.models import LocationInfoDTO
from tabulate import tabulate


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
        data = [
            ["Страна", self.location_info.location.name],
            ["Столица", self.location_info.location.capital],
            ["Регион", self.location_info.location.subregion],
            ["Языки", await self._format_languages()],
            ["Население страны", f"{await self._format_population()} чел."],
            ["Курсы валют", await self._format_currency_rates()],
            ["Площадь страны", f"{self.location_info.location.area} км^2"],
            ["", ""],
            ["Температура", self.location_info.weather.temp],
            ["Описание", self.location_info.weather.description],
            ["Скорость ветра", self.location_info.weather.wind_speed],
            ["Видимость", self.location_info.weather.visible],
            ["Часовой пояс (UTC)", self.location_info.weather.timezone],
            ["Время", self.location_info.weather.time],
        ]
        table = tabulate(data, headers=["Характеристика", "Значение"], tablefmt="pretty")

        dataNews = []
        for i in self.location_info.news:
            news = [i.source, i.title, i.publishDate]
            dataNews.append(news)
        tableNews = tabulate(dataNews, headers=["Источник", "Заголовок", "Дата"], tablefmt="pretty")

        return table, tableNews

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
