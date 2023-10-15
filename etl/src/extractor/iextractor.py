import datetime as dt
from abc import ABC, abstractmethod
from typing import AsyncIterable

from .datatypes import InfoRecord


class BaseExtractor(ABC):
    @abstractmethod
    async def extract_records(self, newer_than: dt.datetime) -> AsyncIterable[InfoRecord]:
        """Extract records from database."""
        raise NotImplementedError
