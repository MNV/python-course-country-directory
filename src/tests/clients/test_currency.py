"""
Тестирование функций клиента для получения информации о курсах валют.
"""
import pytest

from clients.currency import CurrencyClient


@pytest.mark.asyncio
class TestClientCurrency:
    """
    Тестирование клиента для получения информации о валюте.
    """

    base_url = "https://api.apilayer.com/fixer/latest"

    @pytest.fixture
    def client(self):
        return CurrencyClient()

    @pytest.mark.asyncio
    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    @pytest.mark.asyncio
    async def test_get_currency(self, mocker, client):
        mocker.patch("clients.base.BaseClient._request")
        await client.get_rates()
        await client._request(f"{self.base_url}?base=rub")
        await client.get_rates("test")
        await client._request(f"{self.base_url}?base=test")
