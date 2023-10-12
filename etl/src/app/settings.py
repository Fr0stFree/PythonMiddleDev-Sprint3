from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	postgres_user: str
	postgres_password: str
	postgres_host: str
	postgres_port: int
	postgres_db: str

	@property
	def postgres_dsn(self) -> str:
		return f"postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
