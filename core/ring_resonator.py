"""Кольцевой резонатор: f = c / (n * L). Единицы интерфейса: L в см, f в МГц."""

import math

from .constants import C
from .errors import InputError


def _check_n(n: float) -> None:
    if not math.isfinite(n) or n < 1.0:
        raise InputError("Показатель преломления n должен быть не меньше 1")


def _check_positive(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0:
        raise InputError(f"{name} должна быть больше нуля")


def frequency_mhz_from_length_cm(length_cm: float, n: float) -> float:
    """Частота повторения импульсов (МГц) по длине резонатора (см)."""
    _check_n(n)
    _check_positive(length_cm, "Длина")
    length_m = length_cm / 100.0
    return C / (n * length_m) / 1e6


def length_cm_from_frequency_mhz(frequency_mhz: float, n: float) -> float:
    """Длина резонатора (см) по частоте повторения (МГц)."""
    _check_n(n)
    _check_positive(frequency_mhz, "Частота")
    return C / (n * frequency_mhz * 1e6) * 100.0