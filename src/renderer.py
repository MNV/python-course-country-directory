"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from prettytable import PrettyTable

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

    @staticmethod
    def make_table(data: list, columns: list[str]) -> PrettyTable:
        """
        Форматирование прочитанных данных о сущности.

        :param data: Список строк для отображения.
        :param columns: Список названий столбцов.

        :return: Результат форматирования
        """
        table = PrettyTable(columns)
        for row in data:
            table.add_row(row)
        return table

    async def render_country(self) -> PrettyTable:
        """
        Форматирование прочитанных данных о стране.

        :return: Результат форматирования
        """
        location = self.location_info.location
        data = [
            (
                location.name,
                location.subregion,
                await self._format_none(location.area),
                await self._format_languages(),
                await self._format_population(),
                await self._format_currency_rates(),
            )
        ]
        return self.make_table(
            data,
            [
                "Страна",
                "Регион",
                "Площадь (кв. м.)",
                "Языки",
                "Население страны (чел.)",
                "Курсы валют",
            ],
        )

    async def render_capital(self) -> PrettyTable:
        """
        Форматирование прочитанных данных о столице.

        :return: Результат форматирования
        """
        capital = self.location_info.capital
        data = [
            (
                capital.name,
                await self._format_none(capital.latitude),
                await self._format_none(capital.longitude),
                await self._format_none(capital.timezone),
                await self._format_none(capital.current_time),
            )
        ]
        return self.make_table(
            data,
            [
                "Название столицы",
                "Широта",
                "Долгота",
                "Часовой пояс",
                "Текущее местное время",
            ],
        )

    async def render_weather(self) -> PrettyTable:
        """
        Форматирование прочитанных данных о погоде.

        :return: Результат форматирования
        """
        weather = self.location_info.weather
        data = [
            (weather.description, weather.temp, weather.visibility, weather.wind_speed)
        ]
        return self.make_table(
            data,
            ["Описание", "Температура (°C)", "Видимость (м)", "Скорость ветра (м/с)"],
        )

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

    async def _format_none(self, input_field: str | float | None) -> str | float:
        """
        Форматирование поля, которое может принимать значение None.

        :return:
        """

        return input_field if not None else "Неизвестно"

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
