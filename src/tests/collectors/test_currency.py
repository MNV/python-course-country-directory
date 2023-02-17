"""
Тестирование функций сбора информации о курсах валют.
"""
import json

import aiofiles
import pytest

from collectors.collector import CurrencyRatesCollector


@pytest.mark.asyncio
class TestCollectorCurrency:
    @pytest.fixture(autouse=True)
    def collector(self):
        self.collector = CurrencyRatesCollector()

    @pytest.mark.asyncio
    async def test_read_currencies(self):
        """
        Тестирование чтения информации о валютах.
        """
        currencies = await self.collector.read()
        assert currencies is not None
        assert currencies.base.lower() == "rub"
        assert len(currencies.rates) == 170

    @pytest.mark.asyncio
    async def test_collecting_currencies(self):
        """
        Тестирование получения информации о валютах.
        """
        await self.collector.collect()
        async with aiofiles.open(
            await self.collector.get_file_path(), mode="r"
        ) as file:
            content = await file.read()
        currencies = json.loads(content)
        read_currencies = await self.collector.read()
        assert currencies["base"] == read_currencies.base
        assert len(currencies["rates"]) == len(read_currencies.rates)
