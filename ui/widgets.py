"""Общие виджеты в едином стиле."""

import tkinter as tk

from . import theme


def make_button(parent, text, command, font=theme.F_BUTTON, **kwargs):
    return tk.Button(
        parent, text=text, command=command, font=font,
        bg=theme.ACCENT_BG, fg=theme.FG,
        activebackground="#e2e2e2", activeforeground=theme.FG,
        relief="solid", bd=1, cursor="hand2", **kwargs,
    )


def make_label(parent, text="", font=theme.F_LABEL, fg=theme.FG, **kwargs):
    return tk.Label(parent, text=text, font=font, bg=theme.BG, fg=fg, **kwargs)


def make_frame(parent, **kwargs):
    return tk.Frame(parent, bg=theme.BG, **kwargs)


def make_group(parent, title, **kwargs):
    return tk.LabelFrame(
        parent, text=f" {title} ", font=theme.F_SECTION,
        bg=theme.BG, fg=theme.FG, bd=1, relief="solid",
        padx=16, pady=12, **kwargs,
    )


class InputRow:
    """Строка: подпись, поле ввода, единица измерения."""

    def __init__(self, parent, label, unit, var=None, on_change=None, width=14):
        self.var = var or tk.StringVar()
        self.frame = make_frame(parent)
        self.label = make_label(self.frame, label, theme.F_LABEL, theme.MUTED)
        self.label.pack(anchor="w")
        row = make_frame(self.frame)
        row.pack(anchor="w", pady=(2, 0))
        self.entry = tk.Entry(
            row, textvariable=self.var, width=width, font=theme.F_ENTRY,
            justify="right", bg=theme.BG, fg=theme.FG, relief="solid", bd=1,
            insertbackground=theme.FG,
        )
        self.entry.pack(side="left", ipady=3)
        self.unit = make_label(row, unit, theme.F_UNIT, width=6, anchor="w")
        self.unit.pack(side="left", padx=(6, 0))
        if on_change:
            self.var.trace_add("write", lambda *_: on_change())

    def set_text(self, label, unit):
        self.label.config(text=label)
        self.unit.config(text=unit)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


class ResultRow:
    """Строка результата: подпись, только чтение, единица, кнопка «Копировать»."""

    def __init__(self, parent, label, unit, width=14):
        self.var = tk.StringVar()
        self.frame = make_frame(parent)
        self.label = make_label(self.frame, label, theme.F_LABEL, theme.MUTED)
        self.label.pack(anchor="w")
        row = make_frame(self.frame)
        row.pack(anchor="w", pady=(2, 0))
        self.entry = tk.Entry(
            row, textvariable=self.var, width=width, font=theme.F_ENTRY,
            justify="right", bg=theme.BG, fg=theme.FG, relief="solid", bd=1,
            state="readonly", readonlybackground=theme.BG,
        )
        self.entry.pack(side="left", ipady=3)
        self.unit = make_label(row, unit, theme.F_UNIT, width=6, anchor="w")
        self.unit.pack(side="left", padx=(6, 0))
        make_button(row, "Копировать", self.copy, font=theme.F_SMALL).pack(
            side="left", padx=(6, 0))

    def set(self, text):
        self.var.set(text)

    def set_text(self, label, unit):
        self.label.config(text=label)
        self.unit.config(text=unit)
        
    def copy(self):
        value = self.var.get().replace(" ", "")
        if not value:
            return
        root = self.frame.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
def make_mode_switch(parent, names, variable, command):
    """Ряд кнопок-переключателей режима. Возвращает рамку (её нужно упаковать)."""
    frame = make_frame(parent)
    for i, name in enumerate(names):
        tk.Radiobutton(
            frame, text=name, variable=variable, value=i, command=command,
            indicatoron=False, font=theme.F_SECTION,
            bg=theme.ACCENT_BG, fg=theme.FG, selectcolor="#cfe3f7",
            activebackground="#e2e2e2", relief="solid", bd=1,
            padx=18, pady=6, cursor="hand2",
        ).pack(side="left", padx=4)
    return frame