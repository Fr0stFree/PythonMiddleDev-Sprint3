import asyncio
import datetime as dt
from typing import Self
from uuid import UUID

import asyncpg


class Extractor:
	def __init__(self, dsn: str, loop: asyncio.AbstractEventLoop) -> None:
		self._dsn = dsn
		self._loop = loop

	async def __aenter__(self) -> Self:
		self._connection = await asyncpg.connect(self._dsn)
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
		await self._connection.close()

	async def extract_updated_records(self, newer_than: dt.datetime):

		async with self._connection.cursor() as cursor:
			person_ids = await self._extract_updated_persons(cursor, newer_than)
			# film_work_ids = await self._extract_updated_film_works(cursor, person_ids)
			print(person_ids)


	async def _extract_updated_persons(self, cursor: asyncpg.connection.cursor, newer_than: dt.datetime) -> tuple[UUID]:
		statement = f"""
			SELECT id FROM content.person WHERE modified > {newer_than.timestamp()};
		"""
		await cursor.execute(statement)
		return await cursor.fetchall()

	async def _extract_updated_film_works(
		self,
		cursor: asyncpg.connection.cursor,
		affected_person_ids: tuple[UUID]
	) -> tuple[UUID]:
		statement = f"""
			SELECT fw.id
			FROM content.film_work AS fw
			LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
			WHERE pfw.person_id IN {affected_person_ids};
		"""
		await cursor.execute(statement)
		return await cursor.fetchall()
