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
    actors: list[PersonModel] = Field(default_factory=list)
    writers: list[PersonModel] = Field(default_factory=list)

    def dump(self) -> dict:
        return {
            'id': self.id,
            'imdb_rating': self.imdb_rating,
            'genre': self.genre,
            'title': self.title,
            'description': self.description,
            'director': self.director,
            'actors_names': ', '.join([actor.name for actor in self.actors]),
            'writers_names': ', '.join([writer.name for writer in self.writers]),
            'actors': [actor.model_dump() for actor in self.actors],
            'writers': [writer.model_dump() for writer in self.writers],
        }
