"""
Функции для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
"""
from clients.base import BaseClient
from settings import API_KEY_APILAYER


class CurrencyClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
    """

    headers = {"apikey": API_KEY_APILAYER}

    async def get_base_url(self) -> str:
        return "https://api.apilayer.com/fixer/latest"

    async def get_rates(self, base: str = "rub") -> dict | None:
        """
        Получение данных о курсах валют.

        :param base: Базовая валюта
        :return:
        """
        self.params["base"] = base
        return await self._request(await self.get_base_url())
