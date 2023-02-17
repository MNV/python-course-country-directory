"""
Тестирование функций сбора информации о странах.
"""

import pytest

from collectors.collector import CountryCollector


@pytest.mark.asyncio
class TestCollectorCountry:
    @pytest.fixture(autouse=True)
    def collector(self):
        self.collector = CountryCollector()

    @pytest.mark.asyncio
    async def test_read_countries(self):
        """
        Тестирование чтения информации о стране.
        """
        countries = await self.collector.read()
        assert len(countries) == 49

    @pytest.mark.asyncio
    async def test_collecting_countries(self):
        """
        Тестирование получения информации о стране.
        """
        countries = await self.collector.collect()
        assert len(countries) == 49
