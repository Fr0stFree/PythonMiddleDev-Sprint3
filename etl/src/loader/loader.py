import asyncio
import logging
from asyncio import Semaphore
from types import TracebackType
from typing import Sequence, Optional, Type

from elasticsearch import AsyncElasticsearch
from typing_extensions import Self, Final

from common.decorators import raise_on_error
from common.exceptions import ElasticConnectionError
from .iloader import BaseLoader
from .models import MovieModel


class Loader(BaseLoader):
    SEMAPHORE_LIMIT: Final[int] = 20

    def __init__(self, dsn: str, index: str, schema: dict) -> None:
        self._dsn = dsn
        self._index = index
        self._schema = schema
        self._es: AsyncElasticsearch | None = None
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> Self:
        self._logger.debug("Connecting to %s...", self._dsn)
        self._es = AsyncElasticsearch(self._dsn)
        await self._es.ping()
        self._logger.info("Connected to ElasticSearch successfully.")
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self._logger.debug("Closing connection to ElasticSearch...")
        await self._es.close()
        self._es = None
        self._logger.info("Connection to ElasticSearch closed.")

    async def update_index(self, documents: Sequence[MovieModel]) -> None:
        await self._create_index_if_not_exists()

        semaphore = asyncio.Semaphore(self.SEMAPHORE_LIMIT)

        coroutines = [self._load_document(document, semaphore) for document in documents]
        self._logger.info("Loading %s documents to ElasticSearch...", len(documents))
        await asyncio.gather(*coroutines)
        self._logger.info("Loaded %s documents to ElasticSearch successfully.", len(documents))

    @raise_on_error(ElasticConnectionError("Failed to load document to ElasticSearch"))
    async def _load_document(self, document: MovieModel, semaphore: Semaphore) -> None:
        async with semaphore:
            await self._es.index(index=self._index, id=document.id, body=document.model_dump())

    @raise_on_error(ElasticConnectionError("Failed to create index in ElasticSearch"))
    async def _create_index_if_not_exists(self) -> None:
        self._logger.debug("Checking index '%s' in ElasticSearch...", self._index)
        is_exist = await self._es.indices.exists(index=self._index)
        if not is_exist:
            self._logger.info("Not found index '%s' in ElasticSearch. Creating...", self._index)
            await self._es.indices.create(index=self._index, body=self._schema)
            self._logger.info("Index '%s' created successfully.", self._index)
        else:
            self._logger.info("Index %s already exists in ElasticSearch.", self._index)
