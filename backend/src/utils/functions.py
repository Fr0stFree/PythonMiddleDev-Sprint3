import re


def to_snake_case(string: str) -> str:
    """Преобразует строку в snake_case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()
