import abc
from typing import Any, Dict

from redis import Redis


class BasePersistence(abc.ABC):
    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        raise NotImplementedError


class RedisPersistence(BasePersistence):
    def __init__(self, dsn: str) -> None:
        self._redis = Redis.from_url(dsn)

    def save_state(self, state: Dict[str, Any]) -> None:
        self._redis.set("state", state)

    def retrieve_state(self) -> Dict[str, Any]:
        return self._redis.get("state")
