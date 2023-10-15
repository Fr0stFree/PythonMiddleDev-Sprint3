import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Dict, Final, Type, Optional

import redis.asyncio as aioredis
from typing_extensions import Self


class BasePersistence(ABC):
    @abstractmethod
    async def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        raise NotImplementedError


class RedisPersistence(BasePersistence):
    STATE_KEY: Final[str] = "state"

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> Self:
        self._logger.debug("Connecting to %s...", self._dsn)
        self._redis = await aioredis.from_url(self._dsn)
        await self._redis.ping()
        self._logger.info("Connected to Redis successfully.")
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self._logger.debug("Closing connection to Redis...")
        await self._redis.close()
        self._redis = None
        self._logger.info("Connection to Redis closed.")

    async def save_state(self, state: Dict[str, Any]) -> None:
        self._logger.debug("Saving state to Redis: <%s>...", state)
        await self._redis.hset(self.STATE_KEY, mapping=state)
        self._logger.info("State saved successfully.")

    async def retrieve_state(self) -> Dict[str, Any]:
        self._logger.debug("Retrieving '%s' state from Redis...", self.STATE_KEY)
        state = await self._redis.hgetall(self.STATE_KEY)
        self._logger.info("Retrieved '%s' state successfully. State: <%s>", self.STATE_KEY, state)
        return state
