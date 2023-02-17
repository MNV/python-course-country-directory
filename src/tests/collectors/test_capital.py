"""
Тестирование функций сбора информации о странах.
"""

import pytest

from collectors.collector import CapitalCollector


@pytest.mark.asyncio
class TestCollectorCapital:
    @pytest.fixture(autouse=True)
    def collector(self):
        self.collector = CapitalCollector()

    @pytest.mark.asyncio
    async def test_read_capital(self):
        """
        Тестирование чтения информации о стране.
        """
        capital = await self.collector.collect("Moscow")
        assert capital is not None
        assert capital.name == "Moscow"
        assert round(capital.latitude, 2) == 55.75
        assert round(capital.longitude, 2) == 37.62
        assert capital.timezone == "Europe/Moscow"
        assert capital.current_time is not None
