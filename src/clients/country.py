"""
Функции для взаимодействия с внешним сервисом-провайдером данных о странах.
"""
from clients.base import BaseClient
from settings import API_KEY_APILAYER


class CountryClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о странах.
    """

    headers = {"apikey": API_KEY_APILAYER}

    async def get_base_url(self) -> str:
        return "https://api.apilayer.com/geo/country"

    async def get_countries(self, bloc: str = "eu") -> dict | None:
        """
        Получение данных о странах.

        :param bloc: Регион
        :return:
        """
        return await self._request(f"{await self.get_base_url()}/regional_bloc/{bloc}")
