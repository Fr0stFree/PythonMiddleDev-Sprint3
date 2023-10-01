import abc
import json
from typing import Any, Dict


class BaseStorage(abc.ABC):
	"""Абстрактное хранилище состояния.

	Позволяет сохранять и получать состояние.
	Способ хранения состояния может варьироваться в зависимости
	от итоговой реализации. Например, можно хранить информацию
	в базе данных или в распределённом файловом хранилище.
	"""

	@abc.abstractmethod
	def save_state(self, state: Dict[str, Any]) -> None:
		"""Сохранить состояние в хранилище."""

	@abc.abstractmethod
	def retrieve_state(self) -> Dict[str, Any]:
		"""Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
	"""Реализация хранилища, использующего локальный файл.

	Формат хранения: JSON
	"""

	def __init__(self, file_path: str) -> None:
		self.file_path = file_path

	def save_state(self, state: Dict[str, Any]) -> None:
		"""Сохранить состояние в хранилище."""
		json.dump(state, open(self.file_path, 'w'))

	def retrieve_state(self) -> Dict[str, Any]:
		"""Получить состояние из хранилища."""
		return json.load(open(self.file_path, 'r'))


class State:
	"""Класс для работы с состояниями."""

	def __init__(self, storage: BaseStorage) -> None:
		self.storage = storage

	def set_state(self, key: str, value: Any) -> None:
		"""Установить состояние для определённого ключа."""
		self.storage.save_state({key: value})

	def get_state(self, key: str) -> Any:
		"""Получить состояние по определённому ключу."""
		state = self.storage.retrieve_state()
		return state.get(key)
