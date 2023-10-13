from asyncio import iscoroutinefunction
from functools import wraps
from time import sleep
from typing import Callable, Type

from .persistence import BasePersistence


def backoff(
    exception: Type[Exception],
    start_sleep_time: float = 1,
    factor: float = 2,
    border_sleep_time: float = 60,
):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return await func(*args, **kwargs)
                except exception as error:
                    print(f"Encountered error: {error}\nRetrying in {sleep_time} seconds...")
                    sleep(sleep_time)
                    sleep_time = min(sleep_time * factor, border_sleep_time)

        return inner

    return func_wrapper
