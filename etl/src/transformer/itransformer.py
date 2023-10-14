from abc import ABC, abstractmethod
from typing import Sequence

from extractor.datatypes import InfoRecord
from loader.models import MovieModel


class BaseTransformer(ABC):
	@abstractmethod
	def process(self, records: Sequence[InfoRecord]) -> None:
		"""Process records."""
		raise NotImplementedError

	@abstractmethod
	def to_json(self) -> Sequence[MovieModel]:
		"""Return records in format suitable for Elastic."""
		raise NotImplementedError
