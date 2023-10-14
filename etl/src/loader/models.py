from uuid import UUID

from pydantic import BaseModel, Field


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
	actors_names: str = ""
	writers: list[PersonModel] = Field(default_factory=list)
	writers_names: str = ""
