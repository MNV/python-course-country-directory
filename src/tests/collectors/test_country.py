"""
Тестирование функций сбора информации о странах.
"""

import pytest

from collectors.collector import CountryCollector


@pytest.mark.asyncio
class TestClientCountry:
    """
    Тестирование клиента для получения информации о странах.
    """

    @pytest.fixture
    def collector(self):
        return CountryCollector()

    async def test_collect_countries(self, collector):
        result = await collector.collect()

        assert len(result) == 49

    async def test_read_countries(self, collector):
        result = await collector.read()

        assert len(result) == 49
