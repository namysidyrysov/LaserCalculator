import tkinter as tk
from tkinter import ttk
import os
import sys

# Калькулятор кольцевого резонатора
# Формула: f = c/(n*L)

C = 299_792_458.0 # м/с

# def resource_path(relative_path):
#     # 
#     try:
#         base_path=sys._MEIPASS
#     except:
#         base_path=os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

class Resonator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор кольцевого резонатора")
        self.root.geometry('900x900')
        self.root.minsize(600, 600)
        self.root.configure(bw='white')
        
        self.n_var = tk.StringVar(value='1.46')
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
        
        style.configure("White.TFrame", background='white')
        
        


