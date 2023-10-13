import asyncio
import datetime as dt
from typing import Final

from app import Extractor, Transformer, Loader, settings
from app.utils import backoff
from app.persistence import BasePersistence, RedisPersistence


BATCH_SIZE: Final[int] = 100


@backoff(Exception)
async def run_etl(last_modified: dt.datetime) -> None:
    async with Extractor(settings.postgres_dsn) as extractor, Loader(settings.postgres_dsn) as loader:
        transformer = Transformer()

        async for records in extractor.extract_records(newer_than=last_modified, batch_size=BATCH_SIZE):
            transformer.process(records)

        await loader.update_index(
            index=settings.elastic_search_movies_index_name,
            models=transformer.result,
            schema=settings.elastic_search_movies_index_schema,
        )


async def main() -> None:
    persistence: BasePersistence = RedisPersistence(settings.redis_dsn)
    while True:
        state = persistence.retrieve_state()
        last_modified = state.get("last_modified", dt.datetime.min)
        try:
            await run_etl(last_modified)
        except Exception as error:
            print(f"Encountered error: {error}")
        else:
            persistence.save_state({"last_modified": dt.datetime.now()})
            print("Successfully finished ETL cycle")


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(main())
