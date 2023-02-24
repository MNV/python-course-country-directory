import pytest


async def mock_cache_invalid(x, **kwargs):
    return False


@pytest.fixture(autouse=True)
async def mock_requests(mocker):
    mocker.patch("clients.base.BaseClient._request")
    mocker.patch("collectors.base.BaseCollector.cache_invalid", mock_cache_invalid)
    mocker.patch(
        "collectors.collector.WeatherCollector.cache_invalid", mock_cache_invalid
    )
