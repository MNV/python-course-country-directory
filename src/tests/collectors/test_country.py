"""
Тестирование функций сбора информации о странах.
"""
import pytest

from collectors.collector import CountryCollector


class TestCountryCollector:
    """
    Тестирование функций сбора информации о странах.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.collector = CountryCollector()

    @pytest.mark.asyncio
    async def test_collect_country_success(self, mocker):
        """
        Тестирование получения информации о стране.
        """
        countries = await self.collector.collect()
        assert len(countries) == 49

    @pytest.mark.asyncio
    async def test_read_country_success(self, mocker):
        """
        Тестирование чтения информации о стране.
        """
        countries = await self.collector.read()
        assert len(countries) == 49
