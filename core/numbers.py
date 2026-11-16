"""Разбор и форматирование чисел. Не зависит от интерфейса."""

import math
from decimal import Decimal
from typing import Optional

from .errors import InputError


def parse_number(text: str) -> Optional[float]:
    """Превращает строку в положительное число.

    Возвращает None, если поле пустое.
    Бросает InputError, если введено не число, нуль, отрицательное или inf/nan.
    Принимает запятую как разделитель и пробелы как разделители тысяч.
    """
    cleaned = text.strip().replace(",", ".")
    for ch in (" ", "\u00a0", "\u202f"):
        cleaned = cleaned.replace(ch, "")
    if not cleaned:
        return None
    try:
        value = float(cleaned)
    except ValueError:
        raise InputError("Введите число") from None
    if not math.isfinite(value):
        raise InputError("Введите конечное число")
    if value <= 0:
        raise InputError("Значение должно быть больше нуля")
    return value


def format_number(value: float, significant: int = 6) -> str:
    """Форматирует число без экспоненты, с пробелами между тысячами."""
    if value == 0:
        return "0"
    text = f"{value:.{significant}g}"
    text = format(Decimal(text), "f")  # убирает экспоненту
    if "." in text:
        text = text.rstrip("0").rstrip(".")

    sign = ""
    if text.startswith("-"):
        sign, text = "-", text[1:]
    int_part, _, frac_part = text.partition(".")

    groups = []
    while len(int_part) > 3:
        groups.insert(0, int_part[-3:])
        int_part = int_part[:-3]
    groups.insert(0, int_part)

    result = sign + " ".join(groups)
    if frac_part:
        result += "." + frac_part
    return result