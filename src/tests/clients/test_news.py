"""
Тестирование функций клиента для получения информации о новостях.
"""
import pytest

from clients.news import NewsClient
from settings import API_KEY_NEWSAPI


class TestClientNews:
    """
    Тестирование клиента для получения информации о странах.
    """

    base_url = "https://newsapi.org/v2"

    @pytest.fixture
    def client(self):
        return NewsClient()

    @pytest.mark.asyncio
    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    @pytest.mark.asyncio
    async def test_get_countries(self, mocker, client):
        mocker.patch("clients.base.BaseClient._request")
        await client.get_news("ru")
        await client._request(
            f"{self.base_url}/top-headlines?country=ru&apiKey={API_KEY_NEWSAPI}"
        )
