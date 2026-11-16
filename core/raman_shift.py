"""Рамановский сдвиг (Stokes). Длины волн в нм (вакуумные), сдвиг в см^-1.

Δν = 1e7 / λ_накачки − 1e7 / λ_Stokes
"""

import math

from .errors import InputError

NM_TO_CM = 1e7  # 1 см = 1e7 нм


def _check(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0:
        raise InputError(f"{name} должна быть больше нуля")


def stokes_nm_from_pump_and_shift(pump_nm: float, shift_cm1: float) -> float:
    """Длина волны Stokes (нм) по длине волны накачки (нм) и сдвигу (см^-1)."""
    _check(pump_nm, "Длина волны")
    _check(shift_cm1, "Рамановский сдвиг")
    pump_wn = NM_TO_CM / pump_nm
    stokes_wn = pump_wn - shift_cm1
    if stokes_wn <= 0:
        raise InputError(
            f"Сдвиг слишком велик: должен быть меньше {pump_wn:.1f} см⁻¹"
        )
    return NM_TO_CM / stokes_wn


def shift_from_pump_and_stokes(pump_nm: float, stokes_nm: float) -> float:
    """Рамановский сдвиг (см^-1) по длинам волн накачки и Stokes (нм)."""
    _check(pump_nm, "Длина волны")
    _check(stokes_nm, "Длина волны")
    if stokes_nm <= pump_nm:
        raise InputError(
            "Длина волны Stokes должна быть больше длины волны накачки"
        )
    return NM_TO_CM / pump_nm - NM_TO_CM / stokes_nm



def pump_nm_from_stokes_and_shift(stokes_nm: float, shift_cm1: float) -> float:
    """Длина волны накачки (нм) по длине волны Stokes (нм) и сдвигу (см^-1)."""
    _check(stokes_nm, "Длина волны")
    _check(shift_cm1, "Рамановский сдвиг")
    pump_wn = NM_TO_CM / stokes_nm + shift_cm1
    return NM_TO_CM / pump_wn