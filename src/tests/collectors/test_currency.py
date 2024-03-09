"""
Тестирование функций сбора информации о курсах валют.
"""

import pytest

from collectors.collector import CurrencyRatesCollector


@pytest.mark.asyncio
class TestClientCountry:
    """
    Тестирование клиента для получения информации о курсах валют.
    """

    @pytest.fixture
    def collector(self):
        return CurrencyRatesCollector()

    async def test_collect_currency_rates(self, collector):
        await collector.collect()

    async def test_read_currency_rates(self, collector):
        result = await collector.read()

        assert result is not None
        assert result.base == "RUB"
        assert len(result.rates) == 170
