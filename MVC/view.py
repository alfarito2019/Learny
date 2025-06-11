# view.py
import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import tkinter.messagebox as msg

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de sesión")
        self.style = Style('flatly')
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack()

        self.doc_label = ttk.Label(self.frame, text="Documento:")
        self.doc_entry = ttk.Entry(self.frame)

        self.pass_label = ttk.Label(self.frame, text="Clave:")
        self.pass_entry = ttk.Entry(self.frame, show="*")

        self.login_button = ttk.Button(self.frame, text="Iniciar sesión")

        self.doc_label.grid(row=0, column=0, sticky="e")
        self.doc_entry.grid(row=0, column=1)
        self.pass_label.grid(row=1, column=0, sticky="e")
        self.pass_entry.grid(row=1, column=1)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def get_credentials(self):
        return self.doc_entry.get(), self.pass_entry.get()

    def set_login_action(self, callback):
        self.login_button.config(command=callback)

    def show_message(self, message):
        tk.messagebox.showinfo("Mensaje", message)
