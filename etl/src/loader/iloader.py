from abc import ABC, abstractmethod
from typing import Sequence

from .models import MovieModel


class BaseLoader(ABC):
	@abstractmethod
	async def update_index(self, documents: Sequence[MovieModel]) -> None:
		"""Update index in ElasticSearch."""
		raise NotImplementedError
