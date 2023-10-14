from abc import ABC, abstractmethod
from typing import Any, Dict, Final

import redis.asyncio as aioredis
from typing_extensions import Self
from loguru import logger


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

    async def __aenter__(self) -> Self:
        logger.debug(f"Connecting to {self._dsn}...")
        self._redis = await aioredis.from_url(self._dsn)
        await self._redis.ping()
        logger.info("Connected to Redis successfully.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        logger.debug("Closing connection to Redis...")
        await self._redis.close()
        self._redis = None
        logger.info("Connection to Redis closed.")

    async def save_state(self, state: Dict[str, Any]) -> None:
        logger.debug(f"Saving state to Redis: {state}")
        await self._redis.hset(self.STATE_KEY, mapping=state)
        logger.info("State saved successfully.")

    async def retrieve_state(self) -> Dict[str, Any]:
        logger.debug(f"Retrieving {self.STATE_KEY} state from Redis...")
        state = await self._redis.hgetall(self.STATE_KEY)
        logger.info(f"Retrieved {self.STATE_KEY} state successfully. State: {state}")
        return state
