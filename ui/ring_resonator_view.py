"""Экран «Ring Resonator»: один блок расчёта, два режима."""

import tkinter as tk

from core import ring_resonator as rr
from core.errors import InputError
from core.numbers import format_number, parse_number

from . import theme
from .base import CalculatorView
from .widgets import (InputRow, ResultRow, make_frame, make_group, make_label,
                      make_mode_switch)

DEFAULT_N = "1.46"

# Режим: (кнопка, (подпись входа, ед.), (подпись результата, ед.), функция(value, n))
MODES = [
    ("Найти частоту",
     ("Длина L", "см"),
     ("Частота f", "МГц"),
     rr.frequency_mhz_from_length_cm),
    ("Найти длину",
     ("Частота f", "МГц"),
     ("Длина L", "см"),
     rr.length_cm_from_frequency_mhz),
]


class RingResonatorView(CalculatorView):
    TITLE = "Ring Resonator"
    SUBTITLE = "Частота повторения и длина кольцевого резонатора"

    def build(self, body):
        # Формула
        group = make_group(body, "Формула")
        group.pack(fill="x", pady=(0, 10))
        canvas = tk.Canvas(group, height=70, bg=theme.BG, highlightthickness=0)
        canvas.pack(fill="x")
        canvas.bind("<Configure>", lambda e: self._draw_formula(canvas))
        make_label(group, "f — частота, c — скорость света, "
                          "n — показатель преломления, L — длина",
                   theme.F_LABEL).pack()

        # Константа c и показатель преломления n
        const = make_frame(body)
        const.pack(anchor="w", pady=(0, 8))  # прижата к левому краю
        make_label(const, "Скорость света c:", theme.F_SECTION).grid(
            row=0, column=0)
        make_label(const, "299 792 458 м/с", theme.F_SECTION).grid(
            row=0, column=1, padx=(10, 30))
        make_label(const, "n:", theme.F_SECTION).grid(row=0, column=2)
        # значение по умолчанию задаём заранее, чтобы не вызвать пересчёт
        # до создания остальных полей
        self.n_row = InputRow(const, "", "", var=tk.StringVar(value=DEFAULT_N),
                              on_change=self.recalc, width=6)
        self.n_row.label.pack_forget()  # пустая подпись не нужна
        self.n_row.unit.pack_forget()   # пустая единица не нужна
        self.n_row.frame.grid(row=0, column=3, padx=(8, 0))

        # Переключатель режима
        self.mode_var = tk.IntVar(value=0)
        make_mode_switch(body, [m[0] for m in MODES], self.mode_var,
                         self.on_mode).pack(pady=(4, 8))

        self.error_label = make_label(body, "", theme.F_LABEL, theme.ERROR)
        self.error_label.pack(anchor="w")

        # Единый блок расчёта
        calc = make_group(body, "Расчёт")
        calc.pack(fill="x")
        self.in1 = InputRow(calc, "", "", on_change=self.recalc)
        self.in1.pack(anchor="w")
        self.out = ResultRow(calc, "", "")
        self.out.pack(anchor="w", pady=(10, 0))

        self.on_mode()

    @staticmethod
    def _draw_formula(canvas):
        canvas.delete("all")
        cx = canvas.winfo_width() / 2 + 20
        f = "Times New Roman"
        canvas.create_text(cx, 16, text="c", font=(f, 19, "bold"))
        canvas.create_line(cx - 34, 33, cx + 34, 33, width=2)
        canvas.create_text(cx, 50, text="n · L", font=(f, 17, "bold"))
        canvas.create_text(cx - 48, 34, text="f =", font=(f, 19, "bold"), anchor="e")

    # --- режимы
    def on_mode(self):
        _, inp, res, _ = MODES[self.mode_var.get()]
        self.in1.set_text(*inp)
        self.out.set_text(*res)
        self.clear_fields()

    def recalc(self):
        func = MODES[self.mode_var.get()][3]
        try:
            value = parse_number(self.in1.var.get())
            n = parse_number(self.n_row.var.get())
            if value is None or n is None:
                self.out.set("")
                self._set_error("")
                return
            self.out.set(format_number(func(value, n)))
            self._set_error("")
        except InputError as e:
            self.out.set("")
            self._set_error(str(e))

    def _set_error(self, text):
        self.error_label.config(text=text)

    def clear_fields(self):
        """Очищает вход и результат, n не трогает."""
        self.in1.var.set("")
        self.out.set("")
        self._set_error("")
        self.in1.entry.focus_set()

    def clear(self):
        """Кнопка «Очистить»: всё, включая возврат n к значению по умолчанию."""
        self.n_row.var.set(DEFAULT_N)
        self.clear_fields()