from typing import Sequence
from uuid import UUID

from loguru import logger
from typing_extensions import Self

from extractor.datatypes import InfoRecord
from loader.models import PersonModel, MovieModel
from .itransformer import BaseTransformer


class Transformer(BaseTransformer):
    def __enter__(self) -> Self:
        self._model_storage: dict[UUID, MovieModel] = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._model_storage.clear()

    def process(self, records: Sequence[InfoRecord]) -> None:
        for record in records:
            model = self._get_model(record)
            self._enrich_model(model, record)
            self._save_model(model)

        logger.info(f"Transformed {len(records)} records successfully. Total transformed: {len(self._model_storage)}")

    def _get_model(self, record: InfoRecord) -> MovieModel:
        if (model := self._model_storage.get(record["film_work_id"])) is not None:
            return model
        return MovieModel(
            id=record["film_work_id"],
            imdb_rating=record["film_work_rating"],
            title=record["film_work_title"],
            description=record["film_work_description"],
            genre=record["genre_name"],
        )

    def _save_model(self, model: MovieModel) -> None:
        self._model_storage[model.id] = model

    def _enrich_model(self, model: MovieModel, record: InfoRecord) -> None:
        match record["person_film_work_role"]:
            case "director":
                model.director = record["person_full_name"]

            case "actor":
                person = PersonModel(id=record["person_id"], name=record["person_full_name"])
                model.actors.append(person)
                model.actors_names = ", ".join([person.name for person in model.actors])

            case "writer":
                person = PersonModel(id=record["person_id"], name=record["person_full_name"])
                model.writers.append(person)
                model.writers_names = ", ".join([person.name for person in model.writers])

    def to_json(self) -> list[MovieModel]:
        logger.debug(f"Converting {len(self._model_storage)} models to JSON...")
        return list(self._model_storage.values())
