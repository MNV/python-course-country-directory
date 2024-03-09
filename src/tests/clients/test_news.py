"""
Тестирование функций клиента для получения информации о новостях.
"""

import pytest

from clients.news import NewsClient
from settings import API_KEY_NEWS


@pytest.mark.asyncio
class TestClientNews:
    """
    Тестирование клиента для получения информации о новостях.
    """

    base_url = "https://newsapi.org/v2/top-headlines"

    @pytest.fixture
    def client(self):
        return NewsClient()

    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    async def test_get_news(self, mocker, client):
        mocker.patch("clients.news.NewsClient._request")
        await client.get_news("ru")
        client._request.assert_called_once_with(
            f"{self.base_url}?pageSize=3&page=1&country=ru&apiKey={API_KEY_NEWS}"
        )
