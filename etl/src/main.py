import asyncio

from loguru import logger

from core import Settings
from core.persistence import RedisPersistence
from etl import run_etl
from extractor import Extractor
from loader import Loader
from transformer import Transformer


async def main() -> None:
    settings = Settings()

    async with (
        Extractor(settings.postgres_dsn) as extractor,
        Loader(settings.elastic_dsn, *settings.elastic_index) as loader,
        RedisPersistence(settings.redis_dsn) as persistence,
    ):
        while True:
            try:
                with Transformer() as transformer:
                    await run_etl(extractor, transformer, loader, persistence)
            except Exception as error:
                logger.exception(error)
                timeout = settings.etl_interval.total_seconds() * 3
                logger.error(f"Encountered an unexpected error. Retrying in {timeout} seconds...")
            else:
                timeout = settings.etl_interval.total_seconds()
                logger.info(f"ETL cycle completed successfully. Sleeping for {timeout} seconds...")
            finally:
                await asyncio.sleep(timeout)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(main())
