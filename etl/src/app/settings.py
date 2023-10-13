from pathlib import Path
import json

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).parent.parent

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    elastic_search_host: str
    elastic_search_port: int
    elastic_search_movies_index_name: str = "movies"
    elastic_search_movies_index_schema: dict = json.loads(
        (base_dir / "app" / "elastic_movies_schema.json").read_text()
    )

    @property
    def postgres_dsn(self) -> str:
        return f"postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def elastic_dsn(self) -> str:
        return f"http://{self.elastic_search_host}:{self.elastic_search_port}"


settings = Settings()
