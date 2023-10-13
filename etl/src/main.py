import asyncio
import datetime as dt
from typing import Final

from app import Extractor, Transformer, Loader, settings


BATCH_SIZE: Final[int] = 100


async def main() -> None:
    transformer = Transformer()

    async with Extractor(settings.postgres_dsn) as extractor:
        async for records in extractor.extract_records(newer_than=dt.datetime.min, batch_size=BATCH_SIZE):
            transformer.process(records)

    transformed_records = transformer.result

    async with Loader(settings.elastic_dsn) as loader:
        await loader.update_index(
            index=settings.elastic_search_movies_index_name,
            models=transformed_records,
            schema=settings.elastic_search_movies_index_schema,
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(main())
