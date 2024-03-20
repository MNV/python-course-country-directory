"""
Запуск приложения.
"""

import asyncclick as click

from reader import Reader
from renderer import Renderer


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
    Поиск и вывод информации о стране, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)
    if location_info:
        renderer = Renderer(location_info)
        table, tableNews = await renderer.render()
        
        # Разделение таблицы на строки по переносам строк
        table_lines = table.split('\n')
        
        for line in table_lines:
            click.secho(line, fg="green")
        table_lines_news = tableNews.split('\n')
        for line in table_lines_news:
            click.secho(line, fg="green")
        
    else:
        click.secho("Информация отсутствует.", fg="yellow")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
