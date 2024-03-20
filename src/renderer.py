"""
Функции для формирования выходной информации.
"""
import datetime
from decimal import ROUND_HALF_UP, Decimal

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
        render_information_country = {
            "Страна": self.location_info.location.name,
            "Площадь": self.location_info.location.area,
            "Регион": self.location_info.location.subregion,
            "Языки": await self._format_languages(),
            "Население страны": await self._format_population(),
            "Курсы валют": await self._format_currency_rates(),

            "Столица": self.location_info.location.capital,
            "Широта": self.location_info.location.latitude,
            "Долгота": self.location_info.location.longitude,

            "Погода": self.location_info.weather.temp,
            "Время": await self._format_current_time(),
            "Часовой пояс": await self._get_timezone(),
            "Описание погоды": self.location_info.weather.description,
            "Видимость": self.location_info.weather.visibility,
            "Влажность": self.location_info.weather.humidity,
            "Скорость ветра": self.location_info.weather.wind_speed,
            "Давление": self.location_info.weather.pressure,
        }

        first_column_width = max(len(key) for key in render_information_country) + 1
        second_column_width = max(len(str(value)) for value in render_information_country.values()) + 1
        formatted_render_information_country = [("-" * (first_column_width + second_column_width + 3))]
        formatted_render_information_country.extend(
            [
                f"|{key:<{first_column_width}}|{value:>{second_column_width}}|"
                for key, value in render_information_country.items()
            ])
        formatted_render_information_country.append("-" * (first_column_width + second_column_width + 3))

        return tuple(formatted_render_information_country)

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _get_timezone(self) -> str:
        """
        Форматирование информации о времени.

        :return:
        """
        offset_hours = self.location_info.weather.offset_seconds / 3600.0
        return "UTC{:+d}:{:02d}".format(int(offset_hours), int((offset_hours % 1) * 60))

    async def _format_current_time(self) -> str:
        """
        Форматирование информации о времени.
        :return:
        """

        render_time=datetime.datetime.now() + datetime.timedelta(
            seconds=self.location_info.weather.offset_seconds)
        return render_time.strftime("%X, %x")

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
