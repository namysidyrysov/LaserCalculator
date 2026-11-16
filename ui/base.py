"""Базовый класс калькулятора. Новый калькулятор наследуется от него."""

import tkinter as tk

from . import theme
from .widgets import make_button, make_frame, make_label


class CalculatorView(tk.Frame):
    TITLE = ""
    SUBTITLE = ""  # не показывается, оставлен для будущего

    def __init__(self, parent, on_back):
        super().__init__(parent, bg=theme.BG)
        self.on_back = on_back

        # Верхняя строка: кнопка слева, название по центру
        header = make_frame(self)
        header.pack(fill="x", padx=22, pady=(10, 6))
        header.columnconfigure(0, weight=1, uniform="h")
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=1, uniform="h")
        make_button(header, "← Меню", on_back).grid(row=0, column=0, sticky="w")
        make_label(header, self.TITLE, theme.F_TITLE).grid(row=0, column=1)

        # Футер прижат к низу: «Очистить» всегда видна
        footer = make_frame(self)
        footer.pack(side="bottom", fill="x", pady=10)
        make_button(footer, "Очистить", self.clear, padx=24, pady=4).pack()

        self.body = make_frame(self)
        self.body.pack(fill="both", expand=True, padx=22)

        self.build(self.body)

    def build(self, body):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError