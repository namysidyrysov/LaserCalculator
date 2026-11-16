"""Экран «Raman Shift»: один блок расчёта, три режима."""

import tkinter as tk
from tkinter import font as tkfont

from core import raman_shift as rs
from core.errors import InputError
from core.numbers import format_number, parse_number

from . import theme
from .base import CalculatorView
from .widgets import InputRow, ResultRow, make_frame, make_group, make_label

# Режим: (кнопка, (подпись1, ед.1), (подпись2, ед.2), (подпись результата, ед.), функция)
# Функция получает значения двух полей по порядку.
MODES = [
    ("Найти Stokes",
     ("Длина волны накачки λp", "нм"),
     ("Рамановский сдвиг Δν", "см⁻¹"),
     ("Длина волны Stokes λS", "нм"),
     rs.stokes_nm_from_pump_and_shift),
    ("Найти накачку",
     ("Длина волны Stokes λS", "нм"),
     ("Рамановский сдвиг Δν", "см⁻¹"),
     ("Длина волны накачки λp", "нм"),
     rs.pump_nm_from_stokes_and_shift),
    ("Найти сдвиг",
     ("Длина волны накачки λp", "нм"),
     ("Длина волны Stokes λS", "нм"),
     ("Рамановский сдвиг Δν", "см⁻¹"),
     rs.shift_from_pump_and_stokes),
]


class RamanShiftView(CalculatorView):
    TITLE = "Raman Shift"
    SUBTITLE = "Длина волны накачки, длина волны Stokes и рамановский сдвиг"

    def build(self, body):
        # Формула
        group = make_group(body, "Формула")
        group.pack(fill="x", pady=(0, 10))
        canvas = tk.Canvas(group, height=70, bg=theme.BG, highlightthickness=0)
        canvas.pack(fill="x")
        canvas.bind("<Configure>", lambda e: self._draw_formula(canvas))
        make_label(
            group,
            "Δν — сдвиг (см⁻¹), λp — длина волны накачки, "
            "λS — длина волны Stokes (нм), 10⁷ — перевод нм в см",
            theme.F_SMALL,
        ).pack()

        # Переключатель режима
        self.mode_var = tk.IntVar(value=0)
        switch = make_frame(body)
        switch.pack(pady=(4, 8))
        for i, mode in enumerate(MODES):
            tk.Radiobutton(
                switch, text=mode[0], variable=self.mode_var, value=i,
                command=self.on_mode, indicatoron=False, font=theme.F_SECTION,
                bg=theme.ACCENT_BG, fg=theme.FG, selectcolor="#cfe3f7",
                activebackground="#e2e2e2", relief="solid", bd=1,
                padx=18, pady=6, cursor="hand2",
            ).pack(side="left", padx=4)

        self.error_label = make_label(body, "", theme.F_LABEL, theme.ERROR)
        self.error_label.pack(anchor="w")

        # Единый блок расчёта
        calc = make_group(body, "Расчёт")
        calc.pack(fill="x")
        self.in1 = InputRow(calc, "", "", on_change=self.recalc)
        self.in1.pack(anchor="w")
        self.in2 = InputRow(calc, "", "", on_change=self.recalc)
        self.in2.pack(anchor="w", pady=(10, 0))
        self.out = ResultRow(calc, "", "")
        self.out.pack(anchor="w", pady=(20, 0))

        self.on_mode()

    @staticmethod
    def _draw_formula(canvas):
        """Δν = 10⁷/λp − 10⁷/λS, нарисовано дробями."""
        canvas.delete("all")
        fam = "Times New Roman"
        big = tkfont.Font(family=fam, size=18, weight="bold")
        sub = tkfont.Font(family=fam, size=11, weight="bold")
        mid_y, gap = 34, 10
        num = "10⁷"

        def den_width(s):
            return big.measure("λ") + sub.measure(s)

        frac_w = max(big.measure(num), den_width("p"), den_width("S")) + 12
        items = [("text", "Δν ="), ("frac", "p"), ("text", "−"), ("frac", "S")]
        widths = [big.measure(v) if k == "text" else frac_w for k, v in items]
        total = sum(widths) + gap * (len(items) - 1)
        x = (canvas.winfo_width() - total) / 2

        for (kind, val), w in zip(items, widths):
            if kind == "text":
                canvas.create_text(x, mid_y, text=val, font=big, anchor="w")
            else:
                cx = x + w / 2
                canvas.create_text(cx, mid_y - 16, text=num, font=big)
                canvas.create_line(x, mid_y, x + w, mid_y, width=2)
                dx = cx - den_width(val) / 2
                canvas.create_text(dx, mid_y + 17, text="λ", font=big, anchor="w")
                canvas.create_text(dx + big.measure("λ"), mid_y + 22,
                                   text=val, font=sub, anchor="w")
            x += w + gap

    # --- режимы
    def on_mode(self):
        _, a, b, res, _ = MODES[self.mode_var.get()]
        self.in1.set_text(*a)
        self.in2.set_text(*b)
        self.out.set_text(*res)
        self.clear()

    def recalc(self):
        func = MODES[self.mode_var.get()][4]
        try:
            a = parse_number(self.in1.var.get())
            b = parse_number(self.in2.var.get())
            if a is None or b is None:
                self.out.set("")
                self._set_error("")
                return
            self.out.set(format_number(func(a, b)))
            self._set_error("")
        except InputError as e:
            self.out.set("")
            self._set_error(str(e))

    def _set_error(self, text):
        self.error_label.config(text=text)

    def clear(self):
        self.in1.var.set("")
        self.in2.var.set("")
        self.out.set("")
        self._set_error("")
        self.in1.entry.focus_set()