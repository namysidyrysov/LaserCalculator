import tkinter as tk
from tkinter import ttk
import os
import sys

# КАЛЬКУЛЯТОР КОЛЬЦЕВОГО РЕЗОНАТОРА
# Формула: f = c / (n * L)


C = 299_792_458.0  # м/с


def resource_path(relative_path):
    """Работает и в .py, и внутри собранного .exe."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



class ResonatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор кольцевого резонатора")
        self.root.geometry("900x700")
        self.root.minsize(600, 600)
        self.root.configure(bg="white")

        self.n_var = tk.StringVar(value="1.46")
        self.length_input_var = tk.StringVar()
        self.frequency_from_length_var = tk.StringVar()
        self.frequency_input_var = tk.StringVar()
        self.length_from_frequency_var = tk.StringVar()

        self.updating = False

        self.setup_style()
        self.build_ui()
        self.bind_events()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("White.TFrame",   background="white")
        style.configure("White.TLabel",   background="white", foreground="black")
        style.configure("White.TLabelframe",       background="white")
        style.configure("White.TLabelframe.Label", background="white", foreground="black")

        style.configure("Title.TLabel",    background="white", foreground="black",
                        font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background="white", foreground="black",
                        font=("Segoe UI", 15))
        style.configure("Section.TLabel",  background="white", foreground="black",
                        font=("Segoe UI", 14, "bold"))
        style.configure("Normal.TLabel",   background="white", foreground="black",
                        font=("Segoe UI", 11))
        style.configure("Unit.TLabel",     background="white", foreground="black",
                        font=("Segoe UI", 14))
        style.configure("Small.TLabel",    background="white", foreground="black",
                        font=("Segoe UI", 10))

        style.configure("FormulaHint.TLabel",
                        font=("Segoe UI", 15),
                        background="white",
                        foreground="black")

        # Кнопки — обычные ttk.Button, но зададим отступы
        style.configure("Action.TButton", font=("Segoe UI", 11), padding=6)
        style.configure("Copy.TButton",   font=("Segoe UI", 10), padding=2)


    def build_ui(self):
        main = ttk.Frame(self.root, padding=22, style="White.TFrame")
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Калькулятор кольцевого резонатора",
                  style="Title.TLabel").pack(pady=(0, 3))

        ttk.Label(main, text="Автоматический расчёт длины и частоты",
                  style="Subtitle.TLabel").pack(pady=(0, 15))

        # ----------------------------------------------------
        # Формула
        # ----------------------------------------------------
        formula_frame = tk.LabelFrame(
            main, text=" Формула ",
            font=("Segoe UI", 15, "bold"),
            padx=15, pady=8,
            bg="white", fg="black",
            bd=1, relief="solid"
        )
        formula_frame.pack(fill="x", pady=(0, 12))

        formula_canvas = tk.Canvas(formula_frame, height=115, bg="white",
                                   highlightthickness=0)
        formula_canvas.pack(fill="x")

        def draw_fraction(event=None):
            formula_canvas.delete("all")
            w = formula_canvas.winfo_width()
            cx = w / 2 + 30
            formula_canvas.create_text(cx, 36, text="c",
                font=("Times New Roman", 30, "bold"), fill="black")
            formula_canvas.create_line(cx - 48, 56, cx + 48, 56,
                width=2, fill="black")
            formula_canvas.create_text(cx, 82, text="n · L",
                font=("Times New Roman", 27, "bold"), fill="black")
            formula_canvas.create_text(cx - 70, 58, text="f =",
                font=("Times New Roman", 30, "bold"),
                anchor="e", fill="black")

        formula_canvas.bind("<Configure>", draw_fraction)

        ttk.Label(
            formula_frame,
            text="f — частота, c — скорость света, n — показатель преломления, L — длина",
            style="FormulaHint.TLabel"
        ).pack(pady=(2, 0))

        # ----------------------------------------------------
        # Постоянная c и n
        # ----------------------------------------------------
        constants = ttk.Frame(main, style="White.TFrame")
        constants.pack(fill="x", pady=(0, 12))

        ttk.Label(constants, text="Скорость света c:",
                  style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(constants, text="299 792 458 м/с",
                  style="Section.TLabel").grid(row=0, column=1, sticky="w", padx=(10, 0))

        n_row = ttk.Frame(constants, style="White.TFrame")
        n_row.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

        ttk.Label(n_row, text="n:", style="Section.TLabel").pack(side="left")

        self.n_entry = tk.Entry(
            n_row,
            textvariable=self.n_var,
            width=6,
            font=("Segoe UI", 14, "bold"),
            justify="right",
            bg="white", fg="black",
            relief="solid", bd=1,
            insertbackground="black"
        )
        self.n_entry.pack(side="left", padx=(10, 0))

        # ----------------------------------------------------
        # Две области расчёта
        # ----------------------------------------------------
        calculations = ttk.Frame(main, style="White.TFrame")
        calculations.pack(fill="both", expand=True, pady=(2, 0))
        calculations.columnconfigure(0, weight=1)
        calculations.columnconfigure(1, weight=1)

        # ===== Левая область =====
        length_frame = tk.LabelFrame(
            calculations, text=" Рассчитать частоту ",
            font=("Segoe UI", 15, "bold"),
            padx=18, pady=15,
            bg="white", fg="black",
            bd=1, relief="solid"
        )
        length_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(length_frame, text="Введите длину L",
                  style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        length_row = ttk.Frame(length_frame, style="White.TFrame")
        length_row.pack(anchor="w")

        self.length_input_entry = tk.Entry(
            length_row, textvariable=self.length_input_var,
            width=12, font=("Segoe UI", 14, "bold"),
            justify="right", bg="white", fg="black",
            relief="solid", bd=1, insertbackground="black"
        )
        self.length_input_entry.pack(side="left")

        ttk.Label(length_row, text="см", style="Unit.TLabel", width=5, anchor="w"
                  ).pack(side="left", padx=(7, 0))

        ttk.Label(length_frame, text="Частота f",
                  style="Section.TLabel").pack(anchor="w", pady=(30, 0))

        freq_res_row = ttk.Frame(length_frame, style="White.TFrame")
        freq_res_row.pack(anchor="w", pady=(7, 0))

        self.frequency_result_entry = tk.Entry(
            freq_res_row, textvariable=self.frequency_from_length_var,
            width=12, font=("Segoe UI", 14, "bold"),
            justify="right", bg="white", fg="black",
            relief="solid", bd=1, state="readonly",
            readonlybackground="white"
        )
        self.frequency_result_entry.pack(side="left")

        ttk.Label(freq_res_row, text="МГц", style="Unit.TLabel", width=5, anchor="w"
                  ).pack(side="left", padx=(7, 0))

        ttk.Button(
            freq_res_row, text="Копировать", style="Copy.TButton",
            command=lambda: self.copy_value(self.frequency_from_length_var)
        ).pack(side="left", padx=(8, 0))

        # ===== Правая область =====
        frequency_frame = tk.LabelFrame(
            calculations, text=" Рассчитать длину ",
            font=("Segoe UI", 15, "bold"),
            padx=18, pady=15,
            bg="white", fg="black",
            bd=1, relief="solid"
        )
        frequency_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(frequency_frame, text="Введите частоту f",
                  style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        frequency_row = ttk.Frame(frequency_frame, style="White.TFrame")
        frequency_row.pack(anchor="w")

        self.frequency_input_entry = tk.Entry(
            frequency_row, textvariable=self.frequency_input_var,
            width=12, font=("Segoe UI", 14, "bold"),
            justify="right", bg="white", fg="black",
            relief="solid", bd=1, insertbackground="black"
        )
        self.frequency_input_entry.pack(side="left")

        ttk.Label(frequency_row, text="МГц", style="Unit.TLabel", width=5, anchor="w"
                  ).pack(side="left", padx=(7, 0))

        ttk.Label(frequency_frame, text="Длина L",
                  style="Section.TLabel").pack(anchor="w", pady=(30, 0))

        length_res_row = ttk.Frame(frequency_frame, style="White.TFrame")
        length_res_row.pack(anchor="w", pady=(7, 0))

        self.length_result_entry = tk.Entry(
            length_res_row, textvariable=self.length_from_frequency_var,
            width=12, font=("Segoe UI", 14, "bold"),
            justify="right", bg="white", fg="black",
            relief="solid", bd=1, state="readonly",
            readonlybackground="white"
        )
        self.length_result_entry.pack(side="left")

        ttk.Label(length_res_row, text="см", style="Unit.TLabel", width=5, anchor="w"
                  ).pack(side="left", padx=(7, 0))

        ttk.Button(
            length_res_row, text="Копировать", style="Copy.TButton",
            command=lambda: self.copy_value(self.length_from_frequency_var)
        ).pack(side="left", padx=(8, 0))

        # ----------------------------------------------------
        # Кнопка «Очистить» (по центру)
        # ----------------------------------------------------
        ttk.Button(
            main, text="Очистить", style="Action.TButton",
            command=self.clear_all
        ).pack(pady=(18, 0), ipadx=20)

      
    def bind_events(self):
        self.length_input_entry.bind("<KeyRelease>", self.calculate_frequency)
        self.frequency_input_entry.bind("<KeyRelease>", self.calculate_length)
        self.n_entry.bind("<KeyRelease>", self.recalculate_from_n)

        self.length_input_entry.bind(
            "<Return>", lambda e: self.frequency_input_entry.focus_set()
        )
        self.frequency_input_entry.bind(
            "<Return>", lambda e: self.length_input_entry.focus_set()
        )

    # --------------------------------------------------------
    # Кнопка «Очистить»
    # --------------------------------------------------------
    def clear_all(self):
        self.length_input_var.set("")
        self.frequency_input_var.set("")
        self.frequency_from_length_var.set("")
        self.length_from_frequency_var.set("")
        self.n_var.set("1.46")   # возвращаем n к значению по умолчанию
        self.length_input_entry.focus_set()

    # --------------------------------------------------------
    # Кнопка «Копировать»
    # --------------------------------------------------------
    def copy_value(self, var):
        value = var.get()
        if not value:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()   # чтобы буфер обмена реально обновился

    @staticmethod
    def parse_number(value):
        value = value.strip().replace(",", ".").replace(" ", "")
        if not value:
            return None
        try:
            number = float(value)
        except ValueError:
            return None
        if number <= 0:
            return None
        return number


    @staticmethod
    def format_number(value):
        if value == 0:
            return "0"

        s = f"{value:.5g}"

        if "e" in s or "E" in s:
            s = f"{value:.10f}".rstrip("0").rstrip(".")

        if "." in s:
            int_part, frac_part = s.split(".")
        else:
            int_part, frac_part = s, ""

        sign = ""
        if int_part.startswith("-"):
            sign, int_part = "-", int_part[1:]

        groups = []
        while len(int_part) > 3:
            groups.insert(0, int_part[-3:])
            int_part = int_part[:-3]
        groups.insert(0, int_part)
        int_part = " ".join(groups)

        result = sign + int_part
        if frac_part:
            result += "." + frac_part
        return result

    def calculate_frequency(self, event=None):
        if self.updating:
            return
        length_cm = self.parse_number(self.length_input_var.get())
        n = self.parse_number(self.n_var.get())
        if length_cm is None or n is None:
            self.frequency_from_length_var.set("")
            return
        length_m = length_cm / 100.0
        frequency_mhz = C / (n * length_m) / 1_000_000.0
        self.frequency_from_length_var.set(self.format_number(frequency_mhz))

    def calculate_length(self, event=None):
        if self.updating:
            return
        frequency_mhz = self.parse_number(self.frequency_input_var.get())
        n = self.parse_number(self.n_var.get())
        if frequency_mhz is None or n is None:
            self.length_from_frequency_var.set("")
            return
        frequency_hz = frequency_mhz * 1_000_000.0
        length_cm = (C / (n * frequency_hz)) * 100.0
        self.length_from_frequency_var.set(self.format_number(length_cm))

    def recalculate_from_n(self, event=None):
        self.calculate_frequency()
        self.calculate_length()


def main():
    root = tk.Tk()

    try:
        root.iconbitmap(resource_path("my_icon.ico"))
    except Exception:
        pass

    ResonatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()