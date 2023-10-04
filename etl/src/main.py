import asyncio

import datetime as dt

from app.settings import settings
from app.extractor import Extractor


async def main() -> None:
	loop = asyncio.get_running_loop()

	async with Extractor(settings.postgres_dsn, loop) as extractor:
		await extractor.extract_updated_records(newer_than=dt.datetime.min)

if __name__ == "__main__":
	loop = asyncio.get_event_loop_policy().new_event_loop()
	loop.run_until_complete(main())
