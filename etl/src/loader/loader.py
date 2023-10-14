import asyncio
from asyncio import Semaphore
from typing import Sequence

from elasticsearch import AsyncElasticsearch
from typing_extensions import Self, Final
from loguru import logger

from common.decorators import raise_on_error
from .exceptions import ElasticConnectionError
from .iloader import BaseLoader
from .models import MovieModel


class Loader(BaseLoader):
    SEMAPHORE_LIMIT: Final[int] = 20

    def __init__(self, dsn: str, index: str, schema: dict) -> None:
        self._dsn = dsn
        self._index = index
        self._schema = schema
        self._es: AsyncElasticsearch | None = None

    async def __aenter__(self) -> Self:
        logger.debug(f"Connecting to {self._dsn}...")
        self._es = AsyncElasticsearch(self._dsn)
        await self._es.ping()
        logger.info("Connected to ElasticSearch successfully.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        logger.debug("Closing connection to ElasticSearch...")
        await self._es.close()
        self._es = None
        logger.info("Connection to ElasticSearch closed.")

    async def update_index(self, documents: Sequence[MovieModel]) -> None:
        await self._create_index_if_not_exists()

        semaphore = asyncio.Semaphore(self.SEMAPHORE_LIMIT)

        coroutines = [self._load_document(document, semaphore) for document in documents]
        logger.info(f"Loading {len(documents)} documents to ElasticSearch...")
        await asyncio.gather(*coroutines)
        logger.info(f"Loaded {len(documents)} documents to ElasticSearch successfully.")

    @raise_on_error(ElasticConnectionError("Failed to load document to ElasticSearch"))
    async def _load_document(self, document: MovieModel, semaphore: Semaphore) -> None:
        async with semaphore:
            await self._es.index(index=self._index, id=document.id, body=document.model_dump())

    @raise_on_error(ElasticConnectionError("Failed to create index in ElasticSearch"))
    async def _create_index_if_not_exists(self) -> None:
        logger.debug(f"Checking index '{self._index}' in ElasticSearch...")
        is_exist = await self._es.indices.exists(index=self._index)
        if not is_exist:
            logger.info(f"Not found index '{self._index}' in ElasticSearch. Creating...")
            await self._es.indices.create(index=self._index, body=self._schema)
            logger.info(f"Index '{self._index}' created successfully.")
        else:
            logger.info(f"Fount index '{self._index}' in ElasticSearch.")
