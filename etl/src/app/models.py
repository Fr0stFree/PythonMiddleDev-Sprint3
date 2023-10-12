from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel, Field


class PersonRecord(TypedDict):
    id: UUID


class FilmWorkRecord(TypedDict):
    id: UUID


class InfoRecord(TypedDict):
    film_work_id: UUID
    film_work_title: str
    film_work_description: str
    film_work_rating: float
    film_work_type: str
    person_film_work_role: str
    person_id: UUID
    person_full_name: str
    genre_name: str


class PersonModel(BaseModel):
    id: UUID
    name: str


class MovieModel(BaseModel):
    id: UUID
    imdb_rating: float
    genre: str
    title: str
    description: str
    director: str = Field(default='')
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)
    actors: list[PersonModel] = Field(default_factory=list)
    writers: list[PersonModel] = Field(default_factory=list)
