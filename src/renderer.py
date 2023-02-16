"""
Функции для формирования выходной информации.
"""

from datetime import datetime, timedelta, tzinfo
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

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

    def decimal_to_dms_with_direction(self, decimal: float, direct: list) -> str:
        """
        Преобразование числа в координаты.

        :param decimal: координата в числовом формате.
        :param direct: список координат направлений
        :return: Координаты в формате (Градусы минуты секунды)
        """
        if decimal >= 0:
            direction = 0 if decimal != 0 else 2
        else:
            direction = 1
        degrees = int(abs(decimal))
        decimal_minutes = (abs(decimal) - degrees) * 60
        minutes = int(decimal_minutes)
        seconds = (decimal_minutes - minutes) * 60
        return f"{degrees}° {minutes}’{seconds:.2f}” {direct[direction]}"

    async def render(self) -> tuple[str, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """
        lon = self.decimal_to_dms_with_direction(
            self.location_info.weather.coord.lon, ["E", "W", ""]
        )
        lat = self.decimal_to_dms_with_direction(
            self.location_info.weather.coord.lat, ["N", "S", ""]
        )
        inf = {
            "Страна": self.location_info.location.name,
            "Столица": self.location_info.location.capital,
            "Площадь": self.location_info.location.area,
            "Регион": self.location_info.location.subregion,
            "Координаты столицы": f"{lat}, {lon}",
            "Языки": f"{await self._format_languages()}",
            "Население страны": f"{await self._format_population()} чел.",
            "Курсы валют": f"{await self._format_currency_rates()}",
        }
        wether = {
            "Температура": f"{self.location_info.weather.temp} °C",
            "Описание погоды": f"{self.location_info.weather.description} ",
            "Видемость": f"{self.location_info.weather.visibility} м.",
            "Скорость ветра": f"{self.location_info.weather.wind_speed} м/с",
        }
        timezone = TimezoneInfo(offset=self.location_info.weather.timezone, name=None)
        time = {
            "Часовой пояс": f"{timezone.utc()}",
            "Текущее время": f"{datetime.now(timezone).strftime('%d.%m.%Y %H:%M')}",
        }
        formatted_values = []
        first_column_width = max(len(key) for key in inf) + 1
        second_column_width = max(len(str(value)) for value in inf.values()) + 1

        async def _format_str(data: dict, data_name: str) -> None:
            formatted_values.append(
                (
                    data_name
                    + "-"
                    * (first_column_width + second_column_width + 3 - len(data_name))
                )
            )
            extend = []
            for key, value in data.items():
                string = str(value)
                extend.append(
                    f"|{key:<{first_column_width}}|{string[:second_column_width]:<{second_column_width}}|"
                )
                next_lines = string[second_column_width:]
                while len(str(next_lines)) != 0:
                    extend.append(
                        f"|{'':<{first_column_width}}|{next_lines[:second_column_width]:<{second_column_width}}|"
                    )
                    next_lines = next_lines[second_column_width:]
            formatted_values.extend(extend)

        await _format_str(inf, "Общая информация")
        await _format_str(time, "Время")
        await _format_str(wether, "Погода")
        news_id = 1
        if self.location_info.news is not None:
            for article in self.location_info.news:
                news = {
                    "Источник": "Нет данных"
                    if article.source is None
                    else article.source,
                    "Автор": "Нет данных" if article.author is None else article.author,
                    "Заголовок": "Нет данных"
                    if article.title is None
                    else article.title,
                    "Описание": "Нет данных"
                    if article.description is None
                    else article.description,
                    "Ссылка": "Нет данных" if article.url is None else article.url,
                    "Дата публикации": "Нет данных"
                    if article.published_at is None
                    else article.published_at,
                }
                await _format_str(news, f"Новость #{news_id}")
                news_id += 1
        return tuple(formatted_values)

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


class TimezoneInfo(tzinfo):
    """
    Собственная таймзона.
    """

    def __init__(self, offset: int, name: str | None) -> None:
        """
        Конструктор.

        :param offset: секунды для таймзоны,
        :param name: название времяной зоны
        :return:
        """
        self.offset = timedelta(seconds=offset)
        self.seconds = offset
        self.name = name or self.__class__.__name__

    def utc(self) -> str:
        """
        Текстовое представление в UTC.

        :return:
        """
        sign = "-" if self.seconds < 0 else "+"
        absolute_seconds = abs(self.seconds)
        hours = absolute_seconds // 3600
        minutes = (absolute_seconds % 3600) // 60
        return f"UTC {sign}{hours:02d}:{minutes:02d}"

    def utcoffset(self, dt: Optional[datetime]) -> timedelta:
        """
        Возвращение offset для UTC.

        :param dt: время.
        :return:
        """
        return self.offset

    def tzname(self, dt: Optional[datetime]) -> str:
        """
        Возвращение имени.

        :param dt: время.
        :return:
        """
        return self.name

    def dst(self, dt: Optional[datetime]) -> timedelta:
        """
        Возвращение разница во времени.


        :param dt: время.
        :return:
        """
        return timedelta(0)
