# Laser Calculator

Калькулятор для работы в лаборатории (Windows 10/11).

## Калькуляторы

- **Ring Resonator** — частота повторения импульсов f = c / (n·L) и обратный расчёт длины резонатора.
- **Raman Shift** — длина волны Stokes, длина волны накачки и рамановский сдвиг:
  Δν = 10⁷/λp − 10⁷/λS (длины волн в нм, вакуумные; сдвиг в см⁻¹).

## Запуск из исходников

Требуется Python 3.12+ (только стандартная библиотека, tkinter).

    python main.py

## Тесты

    python test_core.py

## Сборка .exe

    pip install pyinstaller
    python -m PyInstaller --onefile --windowed --name LaserCalculator --icon icon.ico --add-data "logo_menu.png;." --add-data "icon.ico;." main.py

Готовый файл: `dist/LaserCalculator.exe`.

## Добавить новый калькулятор

1. Расчёты положить в `core/`.
2. Создать класс на основе `CalculatorView` в `ui/`.
3. Добавить одну строку в список `CALCULATORS` в `main.py`.