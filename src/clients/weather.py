"""
Функции для взаимодействия с внешним сервисом-провайдером данных о погоде.
"""
from clients.base import BaseClient
from settings import API_KEY_OPENWEATHER


class WeatherClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о погоде.
    """

    params = {"appid": API_KEY_OPENWEATHER, "units": "metric"}

    async def get_base_url(self) -> str:
        return "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, location: str) -> dict | None:
        """
        Получение данных о погоде.

        :param location: Город и страна
        :return:
        """
        self.params["q"] = location
        return await self._request(await self.get_base_url())
