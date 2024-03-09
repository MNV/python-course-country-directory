"""
Функции для взаимодействия с внешним сервисом-провайдером данных о новостях.
"""
from http import HTTPStatus
from typing import Optional

import aiohttp

from clients.base import BaseClient
from logger import trace_config
from settings import API_KEY_NEWS


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о новостях.
    """

    async def get_base_url(self) -> str:
        return "https://newsapi.org/v2/top-headlines"

    async def _request(self, endpoint: str) -> Optional[dict]:

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint) as response:
                if response.status == HTTPStatus.OK:
                    return (await response.json())["articles"]

                return None

    async def get_news(self, location: str, news_count: int = 3) -> Optional[dict]:
        """
        Получение данных о новостях.

        :param location: Код страны (например: us, ru, ...)
        :param news_count: Максимальное количество новостей
        :return:
        """

        return await self._request(
            f"{await self.get_base_url()}?pageSize={news_count}&page=1&country={location}&apiKey={API_KEY_NEWS}"
        )
