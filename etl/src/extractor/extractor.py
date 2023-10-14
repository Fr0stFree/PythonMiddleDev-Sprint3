import datetime as dt
import logging
from typing import AsyncGenerator

import asyncpg
from typing_extensions import Self

from common.decorators import raise_on_error
from .datatypes import PersonRecord, FilmWorkRecord, InfoRecord
from .iextractor import BaseExtractor
from .exceptions import PostgresConnectionError


logger = logging.getLogger(__name__)


class Extractor(BaseExtractor):
	BATCH_SIZE = 100

	def __init__(self, dsn: str) -> None:
		self._dsn = dsn

	async def __aenter__(self) -> Self:
		logger.debug(f"Connecting to {self._dsn}...")
		self._connection: asyncpg.connection.Connection = await asyncpg.connect(self._dsn)
		logger.info("Connected to PostgreSQL successfully.")
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
		logger.debug("Closing connection to PostgreSQL...")
		await self._connection.close()
		logger.info("Connection to PostgreSQL closed.")

	async def extract_records(self, newer_than: dt.datetime) -> AsyncGenerator[InfoRecord, None]:
		logger.info(f"Extracting records modified since '{newer_than}'...")
		modified_persons = await self._extract_modified_persons(newer_than)
		modified_film_works = await self._extract_film_work_ids_by_related_person(modified_persons)
		async for records in self._extract_records_by_related_film_works(modified_film_works):
			yield records

	@raise_on_error(PostgresConnectionError("Failed to extract persons from PostgreSQL"))
	async def _extract_modified_persons(self, newer_than: dt.datetime) -> list[PersonRecord]:
		statement = f"""
            SELECT id FROM content.person WHERE modified > '{newer_than}';
        """
		person_ids = await self._connection.fetch(statement)
		logger.debug(f"Found {len(person_ids)} modified persons since '{newer_than}'.")
		return person_ids

	@raise_on_error(PostgresConnectionError("Failed to extract film works from PostgreSQL"))
	async def _extract_film_work_ids_by_related_person(self, persons: list[PersonRecord]) -> list[FilmWorkRecord]:
		persons = ", ".join([f"'{record['id']}'" for record in persons])
		statement = f"""
            SELECT fw.id
            FROM content.film_work AS fw
            LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
            WHERE pfw.person_id IN ({persons});
        """
		film_work_ids = await self._connection.fetch(statement)
		logger.debug(f"Found {len(film_work_ids)} modified film works by related persons.")
		return film_work_ids

	@raise_on_error(PostgresConnectionError("Failed to extract records from PostgreSQL"))
	async def _extract_records_by_related_film_works(
		self,
		film_works: list[FilmWorkRecord],
	) -> AsyncGenerator[InfoRecord, None]:
		film_works = ", ".join([f"'{record['id']}'" for record in film_works])
		statement = f"""
            SELECT
                fw.id AS film_work_id,
                fw.title AS film_work_title,
                fw.description AS film_work_description,
                fw.rating AS film_work_rating,
                fw.type AS film_work_type,
                pfw.role AS person_film_work_role,
                p.id AS person_id,
                p.full_name AS person_full_name,
                g.name AS genre_name
            FROM content.film_work AS fw
                LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person AS p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work AS gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre AS g ON g.id = gfw.genre_id
            WHERE fw.id IN ({film_works});
        """
		async with self._connection.transaction():
			result = await self._connection.cursor(statement)
			while records := await result.fetch(self.BATCH_SIZE):
				yield records
