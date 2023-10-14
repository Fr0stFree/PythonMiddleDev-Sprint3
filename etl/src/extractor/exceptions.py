class PostgresConnectionError(Exception):
	"""Raised when the connection to the PostgreSQL database fails."""

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)
