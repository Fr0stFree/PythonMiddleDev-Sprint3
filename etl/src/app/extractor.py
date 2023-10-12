import datetime as dt

import asyncpg
from typing_extensions import Self

from .models import PersonRecord, FilmWorkRecord, InfoRecord


class Extractor:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    async def __aenter__(self) -> Self:
        self._connection: asyncpg.connection.Connection = await asyncpg.connect(self._dsn)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._connection.close()

    async def extract_updated_records(self, newer_than: dt.datetime) -> list[InfoRecord]:
        modified_persons = await self._extract_modified_persons(newer_than)
        modified_persons = [modified_persons[0]]
        modified_film_works = await self._extract_film_work_ids_by_related_person(modified_persons)
        records = await self._extract_records_by_related_film_works(modified_film_works)
        return records

    async def _extract_modified_persons(self, newer_than: dt.datetime) -> list[PersonRecord]:
        statement = f"""
			SELECT id FROM content.person WHERE modified > '{newer_than}';
		"""
        return await self._connection.fetch(statement)

    async def _extract_film_work_ids_by_related_person(self, persons: list[PersonRecord]) -> list[FilmWorkRecord]:
        persons = ", ".join([f"'{record['id']}'" for record in persons])
        statement = f"""
			SELECT fw.id
			FROM content.film_work AS fw
			LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
			WHERE pfw.person_id IN ({persons});
		"""
        return await self._connection.fetch(statement)

    async def _extract_records_by_related_film_works(self, film_works: list[FilmWorkRecord]) -> list[InfoRecord]:
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
			FROM 
				content.film_work AS fw
				LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
				LEFT JOIN content.person AS p ON p.id = pfw.person_id
				LEFT JOIN content.genre_film_work AS gfw ON gfw.film_work_id = fw.id
				LEFT JOIN content.genre AS g ON g.id = gfw.genre_id
			WHERE fw.id IN ({film_works});
			"""
        return await self._connection.fetch(statement)
