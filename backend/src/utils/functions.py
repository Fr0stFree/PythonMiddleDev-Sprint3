import re
from typing import Callable, Sequence, Hashable, TypeVar
from itertools import groupby


_T = TypeVar("_T")


def to_snake_case(string: str) -> str:
    """Преобразует строку в snake_case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()


def group_by(
    objects: Sequence[_T], sort_key: Callable
) -> dict[Hashable, list[_T]]:
    """Группирует объекты по ключу"""
    sorted_objects = sorted(objects, key=sort_key)
    return {
        key: list(objects)
        for key, objects in groupby(sorted_objects, sort_key)
    }
