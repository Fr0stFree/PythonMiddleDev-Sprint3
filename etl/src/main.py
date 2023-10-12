import asyncio
import datetime as dt

from app import Extractor, Transformer, Loader, settings


async def main() -> None:
    async with Extractor(settings.postgres_dsn) as extractor:
        records = await extractor.extract_updated_records(newer_than=dt.datetime.min)

    async with Transformer() as transformer:
        models = transformer.transform_records(records)

    async with Loader(settings.elastic_dsn) as loader:
        await loader.update_index(settings.elastic_search_movies_index, models)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(main())
