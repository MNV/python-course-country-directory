"""
Функции для логирования.
"""
import logging
from types import SimpleNamespace

import aiohttp
from aiohttp import ClientSession, TraceRequestStartParams

from settings import LOGGING_LEVEL


async def on_request_start(
    session: ClientSession, context: SimpleNamespace, params: TraceRequestStartParams
) -> None:
    """
    Действия при выполнении HTTP-запроса.

    :param ClientSession session: Сессия для HTTP-запроса
    :param SimpleNamespace context: Контекст запроса
    :param TraceRequestStartParams params: Параметры запроса
    :return:
    """
    # pylint: disable=unused-argument
    logging.getLogger("aiohttp.client").debug("Starting request <%s>", params)


logging.basicConfig(level=LOGGING_LEVEL)
trace_config = aiohttp.TraceConfig()
trace_config.on_request_start.append(on_request_start)
