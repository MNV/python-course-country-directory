"""
Поиск собранной информации в файлах на диске.
"""

from difflib import SequenceMatcher
from typing import Optional

from collectors.collector import (
    CapitalCollector,
    CountryCollector,
    CurrencyRatesCollector,
    WeatherCollector,
)
from collectors.models import (
    CapitalDTO,
    CountryDTO,
    CurrencyInfoDTO,
    LocationDTO,
    LocationInfoDTO,
    WeatherInfoDTO,
)


class Reader:
    """
    Чтение сохраненных данных.
    """

    async def find(self, location: str) -> Optional[LocationInfoDTO]:
        """
        Поиск данных о стране по строке.

        :param location: Строка для поиска
        :return:
        """

        country = await self.find_country(location)
        if country:
            capital = await self.get_capital(country.capital)
            weather = await self.get_weather(
                LocationDTO(capital=country.capital, alpha2code=country.alpha2code)
            )
            currency_rates = await self.get_currency_rates(country.currencies)

            return LocationInfoDTO(
                location=country,
                capital=capital,
                weather=weather,
                currency_rates=currency_rates,
            )

        return None

    @staticmethod
    async def get_currency_rates(currencies: set[CurrencyInfoDTO]) -> dict[str, float]:
        """
        Чтение и формирование информации о курсах валют.

        :param currencies: Множество с данными о курсах валют
        :return:
        """

        currency_rates = await CurrencyRatesCollector.read()
        result = {}
        for currency in currencies:
            if currency_rates:
                if isinstance(rate := currency_rates.rates.get(currency.code), float):
                    result[currency.code] = 1 / rate

        return result

    @staticmethod
    async def get_weather(location: LocationDTO) -> Optional[WeatherInfoDTO]:
        """
        Получение данных о погоде.

        :param location: Объект локации для получения данных
        :return:
        """
        return await WeatherCollector.read(location=location)

    async def find_country(self, search: str) -> Optional[CountryDTO]:
        """
        Поиск страны.

        :param search: Строка для поиска
        :return:
        """

        if countries := await CountryCollector.read():
            for country in countries:
                if await self._match(search, country):
                    return country

        return None

    @staticmethod
    async def get_capital(capital_name: str) -> CapitalDTO:
        """
        Получение данных о столице.

        :param capital_name: Название столицы
        :return:
        """
        return await CapitalCollector.collect(capital_name)

    @staticmethod
    async def _match(search: str, country: CountryDTO) -> bool:
        """
        Получение факта сходства между переданными строками для поиска страны.

        :param search: Строка для сравнения
        :param CountryDTO country: Данные о стране
        :return:
        """

        words = search.split()
        # степень схожести сравниваемого текста
        ratio = 0.67
        for word in words:
            if any(
                [
                    search.lower() in country.capital.lower()
                    or SequenceMatcher(None, word, country.capital).ratio() > ratio,
                    *[
                        search.lower() in spelling.lower()
                        or SequenceMatcher(None, word, spelling).ratio() > ratio
                        for spelling in country.alt_spellings
                    ],
                ]
            ):
                return True

        return False
