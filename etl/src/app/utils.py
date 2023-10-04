from functools import wraps
from time import sleep


def backoff(*exceptions: Exception, start_sleep_time: float = 1, factor: float = 2, border_sleep_time: float = 60):
	"""
	Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
	Использует наивный экспоненциальный рост времени повтора (factor)
	до граничного времени ожидания (border_sleep_time)

	Формула:
		t = start_sleep_time * (factor ^ n), если t < border_sleep_time
		t = border_sleep_time, иначе
	:param exceptions: исключения, при которых нужно повторять выполнение функции
	:param start_sleep_time: начальное время ожидания
	:param factor: во сколько раз нужно увеличивать время ожидания на каждой итерации
	:param border_sleep_time: максимальное время ожидания
	:return: результат выполнения функции
	"""
	def func_wrapper(func):
		@wraps(func)
		def inner(*args, **kwargs):
			sleep_time = start_sleep_time
			while True:
				try:
					return func(*args, **kwargs)
				except exceptions as error:
					print(f"Encountered error: {error}\nRetrying in {sleep_time} seconds...")
					sleep(sleep_time)
					sleep_time = min(sleep_time * factor, border_sleep_time)
		return inner
	return func_wrapper
