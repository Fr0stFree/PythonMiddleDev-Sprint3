import datetime as dt
from abc import ABC, abstractmethod
from typing import AsyncGenerator

from .datatypes import InfoRecord


class BaseExtractor(ABC):
	@abstractmethod
	async def extract_records(self, newer_than: dt.datetime) -> AsyncGenerator[InfoRecord, None]:
		"""Extract records from database."""
		raise NotImplementedError
