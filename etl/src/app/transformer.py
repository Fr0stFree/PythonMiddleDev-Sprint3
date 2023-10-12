from typing import Sequence
from uuid import UUID

from typing_extensions import Self

from .models import PersonModel, MovieModel, InfoRecord


class Transformer:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def transform_records(self, records: Sequence[InfoRecord]) -> list[MovieModel]:
        """Transforms records from InfoRecord to ElasticMovieModel"""
        results: dict[UUID, MovieModel] = {}

        for record in records:

            if (model := results.get(record['film_work_id'])) is None:
                model = MovieModel(
                    id=record['film_work_id'],
                    imdb_rating=record['film_work_rating'],
                    genre=record['genre_name'],
                    title=record['film_work_title'],
                    description=record['film_work_description'],
                )

            match record['person_film_work_role']:
                case 'director':
                    model.director = record['person_full_name']

                case 'actor':
                    person = PersonModel(id=record['person_id'], name=record['person_full_name'])
                    model.actors.append(person)
                    model.actors_names.append(person.name)

                case 'writer':
                    person = PersonModel(id=record['person_id'], name=record['person_full_name'])
                    model.writers.append(person)
                    model.writers_names.append(person.name)

            results[record['film_work_id']] = model

        return list(results.values())
