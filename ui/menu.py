"""Главное меню."""

import math
import tkinter as tk

from . import theme
from .widgets import make_frame, make_label

LOGO_MAX_HEIGHT = 140  # пикселей; большая картинка уменьшается автоматически


class MainMenu(tk.Frame):
    def __init__(self, parent, items, logo=None):
        """items: список пар (название, функция открытия). logo: tk.PhotoImage или None."""
        super().__init__(parent, bg=theme.BG)

        top_pad = 60
        if logo is not None:
            factor = max(1, math.ceil(logo.height() / LOGO_MAX_HEIGHT))
            self.logo_img = logo.subsample(factor) if factor > 1 else logo
            tk.Label(self, image=self.logo_img, bg=theme.BG).pack(pady=(40, 10))
            top_pad = 0

        make_label(self, "Laser Calculator", theme.F_TITLE).pack(pady=(top_pad, 4))
        make_label(self, "Выберите калькулятор", theme.F_SUBTITLE,
                   theme.MUTED).pack(pady=(0, 30))

        box = make_frame(self)
        box.pack()
        for title, command in items:
            tk.Button(
                box, text=title, command=command, font=theme.F_MENU_BUTTON,
                bg=theme.ACCENT_BG, fg=theme.FG, activebackground="#e2e2e2",
                relief="solid", bd=1, width=22, height=2, cursor="hand2",
            ).pack(pady=12)