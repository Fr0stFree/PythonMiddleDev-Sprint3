class PostgresConnectionError(Exception):
	"""Raised when the connection to the PostgreSQL database fails."""

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


class ElasticConnectionError(ConnectionError):
	"""Raised when the connection to ElasticSearch fails."""

	def __init__(self, message) -> None:
		self.message = message
		super().__init__(self.message)
