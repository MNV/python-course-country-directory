"""
Тестирование клиента для получения информации о новостях.
"""
import pytest

from clients.news import NewsClient


class TestClientCountry:
    """
    Тестирование клиента для получения информации о странах.
    """

    base_url = "https://newsapi.org/v2/everything"

    @pytest.fixture
    def client(self):
        return NewsClient()

    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    async def test_get_countries(self, mocker, client):
        mocker.patch("clients.base.BaseClient._request")
        await client.get_news("test")
        client._request.assert_called_once_with(self.base_url)
        assert client.params["q"] == "test"
