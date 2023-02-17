"""
Запуск приложения.
"""

import asyncclick as click
from prettytable import PrettyTable

from reader import Reader
from renderer import Renderer


def print_info(title: str, render_result: PrettyTable) -> None:
    """
    Вывод информации о сущности в консоль

    :param title: Название таблицы.
    :param render_result: Таблица.
    """

    lines = render_result
    click.secho(title, bold=True, fg="green")
    for line in lines:
        click.secho(line, fg="green")


@click.command()
@click.option(
    "--location",
    "-l",
    "location",
    type=str,
    help="Страна и/или город",
    prompt="Страна и/или город",
)
async def process_input(location: str) -> None:
    """
    Поиск и вывод информации о стране, столице, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)
    if location_info:
        print_info(
            "Информация о стране", await Renderer(location_info).render_country()
        )
        print_info(
            "Информация о столице", await Renderer(location_info).render_capital()
        )
        print_info(
            "Информация о погоде", await Renderer(location_info).render_weather()
        )
    else:
        click.secho("Информация отсутствует.", fg="yellow")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
