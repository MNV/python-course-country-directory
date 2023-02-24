"""
Базовые функции для клиентов внешних сервисов.
"""

from abc import ABC, abstractmethod
from http import HTTPStatus
from logging import getLogger
from typing import Any

import aiohttp

from logger import trace_config

logger = getLogger(__name__)


class BaseClient(ABC):
    """
    Базовый класс, реализующий интерфейс для клиентов.
    """

    params: dict[str, Any] = {}
    headers: dict[str, Any] = {}

    @abstractmethod
    async def get_base_url(self) -> str:
        """
        Получение базового URL для запросов.
        :return:
        """

    async def _request(self, endpoint: str) -> dict | None:
        """
        Формирование и выполнение запроса.
        :param endpoint:
        :return:
        """
        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(
                endpoint, params=self.params, headers=self.headers
            ) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()
                logger.error(
                    "Error: %s %s %s", response.url, response.status, response.reason
                )
                return None
