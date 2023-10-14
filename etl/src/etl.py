import datetime as dt

from common.decorators import backoff
from core import settings
from core.persistence import BasePersistence
from extractor import BaseExtractor
from extractor.exceptions import PostgresConnectionError
from loader import BaseLoader
from loader.exceptions import ElasticConnectionError
from transformer import BaseTransformer


@backoff(PostgresConnectionError, ElasticConnectionError)
async def run_etl(
	extractor: BaseExtractor,
	transformer: BaseTransformer,
	loader: BaseLoader,
	persistence: BasePersistence
) -> None:
	state = await persistence.retrieve_state()
	last_modified = state.get("last_modified", dt.datetime.min)

	async for records in extractor.extract_records(newer_than=last_modified):
		transformer.process(records)

	await loader.update_index(documents=transformer.to_json())
	await persistence.save_state({"last_modified": dt.datetime.now()})
