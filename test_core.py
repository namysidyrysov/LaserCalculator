from core.errors import InputError
from core.numbers import parse_number, format_number
from core import ring_resonator as rr
from core import raman_shift as rs


def close(a, b, tol):
    assert abs(a - b) <= tol, f"{a} != {b} (tol {tol})"


def raises(func, *args):
    try:
        func(*args)
    except InputError:
        return
    raise AssertionError(f"InputError не возникла: {func.__name__}{args}")


# --- разбор и форматирование чисел
assert parse_number("1,46") == 1.46
assert parse_number(" 1 000 ") == 1000.0
assert parse_number("") is None
for bad in ("abc", "-5", "0", "nan", "inf"):
    raises(parse_number, bad)
assert format_number(205.3373) == "205.337"
assert format_number(1234567) == "1 234 570"
assert format_number(0.000001234) == "0.000001234"

# --- кольцевой резонатор
f = rr.frequency_mhz_from_length_cm(100, 1.46)
close(f, 205.3373, 0.001)
close(rr.length_cm_from_frequency_mhz(f, 1.46), 100, 1e-9)
raises(rr.frequency_mhz_from_length_cm, 0, 1.46)
raises(rr.frequency_mhz_from_length_cm, 100, 0.5)

# --- Raman shift (Stokes)
stokes = rs.stokes_nm_from_pump_and_shift(1064, 440)
close(stokes, 1116.26, 0.01)
raises(rs.stokes_nm_from_pump_and_shift, 1064, 10000)

close(rs.shift_from_pump_and_stokes(1064, stokes), 440, 1e-6)
raises(rs.shift_from_pump_and_stokes, 1064, 1064)
raises(rs.shift_from_pump_and_stokes, 1064, 1000)  # короче накачки: не Stokes
close(rs.pump_nm_from_stokes_and_shift(stokes, 440), 1064, 1e-6)

# --- границы и точность
close(rr.frequency_mhz_from_length_cm(1, 1.0), 29979.2458, 0.001)   # n = 1, 1 см
close(rr.length_cm_from_frequency_mhz(rr.frequency_mhz_from_length_cm(37.5, 1.468), 1.468), 37.5, 1e-9)
raises(rr.length_cm_from_frequency_mhz, -1, 1.46)
raises(rr.frequency_mhz_from_length_cm, 100, 0.99)

# круговая проверка Raman: туда и обратно для разных накачек и сдвигов
for pump in (532, 800, 1030, 1064, 1550):
    for shift in (100, 440, 1000, 3000):
        if 1e7 / pump > shift:
            s = rs.stokes_nm_from_pump_and_shift(pump, shift)
            close(rs.shift_from_pump_and_stokes(pump, s), shift, 1e-6)
            close(rs.pump_nm_from_stokes_and_shift(s, shift), pump, 1e-6)

# ввод
assert parse_number("1e3") == 1000.0
assert parse_number("  205,337 ") == 205.337
raises(parse_number, "1.2.3")

print("Все тесты пройдены")