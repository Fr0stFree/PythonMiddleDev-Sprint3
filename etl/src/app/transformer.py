from typing import Sequence
from uuid import UUID

from typing_extensions import Self

from .models import PersonModel, MovieModel, InfoRecord


class Transformer:

    def __init__(self) -> None:
        self._record_storage: dict[UUID, MovieModel] = {}

    def process(self, records: Sequence[InfoRecord]) -> None:
        for record in records:
            if (model := self._record_storage.get(record['film_work_id'])) is None:
                model = MovieModel(
                    id=record['film_work_id'],
                    imdb_rating=record['film_work_rating'],
                    title=record['film_work_title'],
                    description=record['film_work_description'],
                    genre=record['genre_name'],
                )

            match record['person_film_work_role']:
                case 'director':
                    model.director = record['person_full_name']

                case 'actor':
                    person = PersonModel(id=record['person_id'], name=record['person_full_name'])
                    model.actors.append(person)

                case 'writer':
                    person = PersonModel(id=record['person_id'], name=record['person_full_name'])
                    model.writers.append(person)

            self._record_storage[record['film_work_id']] = model

    @property
    def result(self) -> list[MovieModel]:
        return list(self._record_storage.values())
