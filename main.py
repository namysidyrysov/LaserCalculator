"""Точка входа Laser Calculator.

Чтобы добавить новый калькулятор: создать класс на основе CalculatorView
в ui/ и добавить одну строку в CALCULATORS.
"""
import ctypes
import os
import sys
import tkinter as tk

from ui import theme
from ui.menu import MainMenu
from ui.raman_shift_view import RamanShiftView
from ui.ring_resonator_view import RingResonatorView

# (название в меню, класс калькулятора)
CALCULATORS = [
    ("Ring Resonator", RingResonatorView),
    ("Raman Shift", RamanShiftView),
]


def resource_path(relative_path):
    """Работает и в .py, и внутри собранного .exe."""
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


class App:
    def __init__(self, root):
        self.root = root
        root.title("Laser Calculator")
        root.geometry("1000x640")
        root.configure(bg=theme.BG)

        self.logo = None
        try:
            self.logo = tk.PhotoImage(file=resource_path("logo_menu.png"))
        except tk.TclError:
            pass  # нет файла: работаем без логотипа
        try:
            root.iconbitmap(default=resource_path("icon.ico"))  # иконка окна
        except tk.TclError:
            pass

        self.current = None
        self.show_menu()

    def _show(self, frame):
        if self.current is not None:
            self.current.destroy()
        self.current = frame
        frame.pack(fill="both", expand=True)

        # Окно не может быть меньше, чем нужно содержимому (важно при масштабе 125-150 %)
        self.root.update_idletasks()
        need_w = max(frame.winfo_reqwidth(), 700)
        need_h = frame.winfo_reqheight()
        self.root.minsize(need_w, need_h)
        cur_w, cur_h = self.root.winfo_width(), self.root.winfo_height()
        if cur_w < need_w or cur_h < need_h:
            self.root.geometry(f"{max(cur_w, need_w)}x{max(cur_h, need_h)}")

    def show_menu(self):
        items = [(name, lambda cls=cls: self.open_calculator(cls))
                 for name, cls in CALCULATORS]
        self._show(MainMenu(self.root, items, self.logo))

    def open_calculator(self, cls):
        self._show(cls(self.root, on_back=self.show_menu))


def main():
    try:  # чёткий текст и корректный масштаб на экранах 125-150 %
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()