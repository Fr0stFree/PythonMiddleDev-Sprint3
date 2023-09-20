import datetime as dt
import uuid
from contextlib import closing
from dataclasses import dataclass, asdict
from pathlib import Path
from sqlite3 import Connection
from typing import Generator, Sequence, Final
from typing import TypeVar, Type, TypeAlias

from django.conf import settings
from django.db import migrations

from utils.functions import to_snake_case

SQLITE_FILE_PATH: Final[Path] = (
    settings.BASE_DIR / "movies" / "fixtures" / "initial_movies.sqlite"
)
CHUNK_SIZE: Final[int] = 100


class SQLiteBaseModel:
    """Базовая модель для извлечения данных из SQLite"""

    def to_pg_repr(self) -> dict:
        """Возвращает словарь с данными для записи в БД, приведнные к формату PostgreSQL"""
        result = asdict(self)
        if "updated_at" in result:
            result["modified"] = result.pop("updated_at")

        if "created_at" in result:
            result["created"] = result.pop("created_at")

        return result


@dataclass(frozen=True)
class FilmWork(SQLiteBaseModel):
    updated_at: dt.datetime
    created_at: dt.datetime
    id: uuid.UUID
    title: str
    type: str
    description: str
    creation_date: dt.datetime
    rating: float

    def to_pg_repr(self) -> dict:
        result = super().to_pg_repr()
        if result["description"] is None:
            result["description"] = ""
        return result


@dataclass(frozen=True)
class Person(SQLiteBaseModel):
    updated_at: dt.datetime
    created_at: dt.datetime
    id: uuid.UUID
    full_name: str


@dataclass(frozen=True)
class Genre(SQLiteBaseModel):
    updated_at: dt.datetime
    created_at: dt.datetime
    id: uuid.UUID
    name: str


@dataclass(frozen=True)
class GenreFilmWork(SQLiteBaseModel):
    id: uuid.UUID
    created_at: dt.datetime
    film_work_id: uuid.UUID
    genre_id: uuid.UUID


@dataclass(frozen=True)
class PersonFilmWork(SQLiteBaseModel):
    id: uuid.UUID
    created_at: dt.datetime
    role: str
    film_work_id: uuid.UUID
    person_id: uuid.UUID


SQLiteModelLike: TypeAlias = TypeVar(
    "SQLiteModelLike",
    Type[FilmWork],
    Type[Genre],
    Type[GenreFilmWork],
    Type[Person],
    Type[PersonFilmWork],
)
SQLITE_MODELS: Sequence[SQLiteModelLike] = (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)


def sqlite_extractor(
    connection: Connection,
    model: SQLiteModelLike,
    chunk_size: int = 100,
) -> Generator[tuple[SQLiteModelLike, ...], None, None]:
    """Генератор для извлечения данных из SQLite"""
    table_name = to_snake_case(model.__name__)
    fields_to_fetch = list(model.__dataclass_fields__.keys())
    statement = f'SELECT {", ".join(fields_to_fetch)} FROM {table_name}'

    result = connection.execute(statement)

    while chunk := result.fetchmany(chunk_size):
        yield tuple(model(*row) for row in chunk)


def fill_movies(apps, schema_editor) -> None:
    with closing(Connection(SQLITE_FILE_PATH)) as connection:
        for sqlite_model in SQLITE_MODELS:
            Model = apps.get_model("movies", sqlite_model.__name__)  # noqa
            extractor = sqlite_extractor(
                connection, sqlite_model, chunk_size=CHUNK_SIZE
            )

            for chunk in extractor:
                Model.objects.bulk_create(
                    [Model(**item.to_pg_repr()) for item in chunk],
                    ignore_conflicts=True,
                    batch_size=CHUNK_SIZE,
                )


def remove_movies(apps, schema_editor) -> None:
    for schema in SQLITE_MODELS:
        Model = apps.get_model("movies", schema.__name__)  # noqa
        Model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0002_create_tables"),
    ]

    operations = [
        migrations.RunPython(
            code=fill_movies,
            reverse_code=remove_movies,
        ),
    ]
