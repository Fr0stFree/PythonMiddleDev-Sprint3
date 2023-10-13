import asyncio
from asyncio import Semaphore
from typing import Sequence

from elasticsearch import AsyncElasticsearch
from typing_extensions import Self, Final

from .models import MovieModel


class Loader:
    SEMAPHORE_LIMIT: Final[int] = 20

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._es: AsyncElasticsearch | None = None

    async def __aenter__(self) -> Self:
        self._es = AsyncElasticsearch(self._dsn)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._es.close()
        self._es = None

    async def update_index(self, index: str, models: Sequence[MovieModel], schema: dict) -> None:
        await self._create_index_if_not_exists(index, schema)

        semaphore = asyncio.Semaphore(self.SEMAPHORE_LIMIT)
        coroutines = [self._load_document(index, model, semaphore) for model in models]
        await asyncio.gather(*coroutines)

    async def _load_document(self, index: str, movie: MovieModel, semaphore: Semaphore) -> None:
        async with semaphore:
            await self._es.index(index=index, id=movie.id, body=movie.dump())

    async def _create_index_if_not_exists(self, index: str, schema: dict) -> None:
        if not await self._es.indices.exists(index=index):
            await self._es.indices.create(index=index, body=schema)
