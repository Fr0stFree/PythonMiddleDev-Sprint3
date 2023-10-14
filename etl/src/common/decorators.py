from functools import wraps
from time import sleep
from typing import Type, Callable

from loguru import logger


def backoff(
    *exceptions: Type[Exception],
    start_sleep_time: float = 1,
    factor: float = 2,
    border_sleep_time: float = 60,
) -> Callable:
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as error:
                    logger.warning(f"Encountered expected error: {error}. Retrying in {sleep_time} seconds...")
                    sleep(sleep_time)
                    sleep_time = min(sleep_time * factor, border_sleep_time)

        return inner

    return func_wrapper


def raise_on_error(exception: Exception) -> Callable:
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as error:
                raise exception from error

        return inner

    return func_wrapper
