"""
Описание моделей данных (DTO).
"""

from pydantic import Field, BaseModel
from pydantic.schema import Optional


class HashableBaseModel(BaseModel):
    """
    Добавление хэшируемости для моделей.
    """

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))


class LocationDTO(HashableBaseModel):
    """
    Модель локации для получения сведений о погоде.

    .. code-block::

        LocationDTO(
            capital="Mariehamn",
            alpha2code="AX",
        )
    """

    capital: str
    alpha2code: str = Field(min_length=2, max_length=2)  # country alpha‑2 code


class CurrencyInfoDTO(HashableBaseModel):
    """
    Модель данных о валюте.

    .. code-block::

        CurrencyInfoDTO(
            code="EUR",
        )
    """

    code: str


class LanguagesInfoDTO(HashableBaseModel):
    """
    Модель данных о языке.

    .. code-block::

        LanguagesInfoDTO(
            name="Swedish",
            native_name="svenska"
        )
    """

    name: str
    native_name: str


class CountryDTO(BaseModel):
    """
    Модель данных о стране.

    .. code-block::

        CountryDTO(
            capital="Mariehamn",
            alpha2code="AX",
            alt_spellings=[
              "AX",
              "Aaland",
              "Aland",
              "Ahvenanmaa"
            ],
            currencies={
                CurrencyInfoDTO(
                    code="EUR",
                )
            },
            flag="http://assets.promptapi.com/flags/AX.svg",
            languages={
                LanguagesInfoDTO(
                    name="Swedish",
                    native_name="svenska"
                )
            },
            name="\u00c5land Islands",
            population=28875,
            subregion="Northern Europe",
            timezones=[
                "UTC+02:00",
            ],
            area = 1580.0
            latitude = 4.0,
            longitude = -53.0
        )
    """

    capital: str
    alpha2code: str
    alt_spellings: list[str]
    currencies: set[CurrencyInfoDTO]
    flag: str
    languages: set[LanguagesInfoDTO]
    name: str
    population: int
    subregion: str
    timezones: list[str]
    area: Optional[float]


class CurrencyRatesDTO(BaseModel):
    """
    Модель данных о курсах валют.

    .. code-block::

        CurrencyRatesDTO(
            base="RUB",
            date="2022-09-14",
            rates={
                "EUR": 0.016503,
            }
        )
    """

    base: str
    date: str
    rates: dict[str, float]


class CoordInfoDTO(BaseModel):
    """
    Модель координат.

    .. code-block::

        CoordInfoDTO(
            lon = -0.1257,
            lat = 51.5085,
        )
    """

    lon: float
    lat: float


class WeatherInfoDTO(BaseModel):
    """
    Модель данных о погоде.

    .. code-block::

        WeatherInfoDTO(
            coord=CoordInfoDTO(
               lon = -0.1257,
               lat = 51.5085,
           ),
            temp=13.92,
            pressure=1023,
            humidity=54,
            wind_speed=4.63,
            description="scattered clouds",
            visibility=2500,
            timezone=0
        )
    """

    coord: CoordInfoDTO
    temp: float
    pressure: int
    humidity: int
    wind_speed: float
    description: str
    visibility: int
    timezone: int


class NewsInfoDTO(BaseModel):
    """
    Модель данных о новости.

    .. code-block::

       NewsInfoDTO(
            source="CNN"
            author = "Luke McGee, Jack Guy",
            title = "Nicola Sturgeon unexpectedly quits as first minister of Scotland amid swirl of political setbacks,
            citing 'brutality' of public life - CNN",
            description="Nicola Sturgeon, the figurehead of the Scottish independence movement, dramatically announced
            on Wednesday that she would resign after eight years as Scotland's first minister.",
            url="https://www.cnn.com/2023/02/15/uk/nicola-sturgeon-resigns-scotland-intl/index.html",
            publishedAt = "2023-02-15T12:18:00Z"
        )
    """

    source: Optional[str]
    author: Optional[str]
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    published_at: Optional[str]


class LocationInfoDTO(BaseModel):
    """
    Модель данных для представления общей информации о месте.

    .. code-block::

        LocationInfoDTO(
            location=CountryDTO(
                capital="Mariehamn",
                alpha2code="AX",
                alt_spellings=[
                  "AX",
                  "Aaland",
                  "Aland",
                  "Ahvenanmaa"
                ],
                currencies={
                    CurrencyInfoDTO(
                        code="EUR",
                    )
                },
                flag="http://assets.promptapi.com/flags/AX.svg",
                languages={
                    LanguagesInfoDTO(
                        name="Swedish",
                        native_name="svenska"
                    )
                },
                name="\u00c5land Islands",
                population=28875,
                subregion="Northern Europe",
                timezones=[
                    "UTC+02:00",
                ],
            ),
            weather=WeatherInfoDTO(
                temp=13.92,
                pressure=1023,
                humidity=54,
                wind_speed=4.63,
                description="scattered clouds",
            ),
            currency_rates={
                "EUR": 0.016503,
            },
            news = [
                NewsInfoDTO(
                    source="CNN"
                    author = "Luke McGee, Jack Guy",
                    title = "Nicola Sturgeon unexpectedly quits as first minister of Scotland amid swirl of political
                    setbacks, citing 'brutality' of public life - CNN",
                    description="Nicola Sturgeon, the figurehead of the Scottish independence movement, dramatically
                    announced on Wednesday that she would resign after eight years as Scotland's first minister.",
                    url="https://www.cnn.com/2023/02/15/uk/nicola-sturgeon-resigns-scotland-intl/index.html",
                    publishedAt = "2023-02-15T12:18:00Z"
                ),]
        )
    """

    location: CountryDTO
    weather: WeatherInfoDTO
    currency_rates: dict[str, float]
    news: Optional[list[NewsInfoDTO]]
