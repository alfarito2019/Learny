import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import pandas as pd
import tkinter.messagebox as msg
import tkinter as tk  # Agregado para botón con más control visual

# Cargar base de datos
bd_path = "D:/Pasantia/Learny/BD.xlsx"
df = pd.read_excel(bd_path)
df["Cedula"] = df["Cedula"].astype(str).str.replace(".0", "", regex=False)
df["Clave"] = df["Clave"].astype(str).str.replace(".0", "", regex=False)

# Variable global para cédula activa
cliente_activo = None

root = ttk.Window(themename="flatly")
root.geometry("360x750")
root.resizable(False, False)

# Estilos personalizados
style = ttk.Style()
style.configure("DaviviendaRed.TButton", background="#E0111B", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=0, focusthickness=0, focuscolor="none")
style.map("DaviviendaRed.TButton",
    background=[("active", "#C50F17")],
    foreground=[("disabled", "#cccccc")]
)

style.configure("OutlineBlack.TButton", background="white", foreground="black", bordercolor="black", relief="solid", borderwidth=2, font=("Helvetica", 10))
style.map("OutlineBlack.TButton",
    background=[("active", "#f0f0f0")],
    foreground=[("active", "black")]
)

# --------------------------
# UTILIDADES
# --------------------------
def clear():
    for widget in root.winfo_children():
        widget.destroy()

# --------------------------
# PANTALLAS
# --------------------------
def mostrar_pantalla_inicio():
    clear()
    canvas = ttk.Canvas(root, width=360, height=750)
    canvas.pack()

    imagen_inicio = Image.open("D:/Pasantia/Learny/IMG/Imagen1.png").resize((360, 750))
    bg_img1 = ImageTk.PhotoImage(imagen_inicio)
    canvas.create_image(0, 0, anchor="nw", image=bg_img1)
    canvas.bg_img = bg_img1

    ttk.Button(root, command=mostrar_pantalla_login, text="Soy cliente", style="DaviviendaRed.TButton").place(x=80, y=562, width=200, height=33)
    ttk.Button(root, command=lambda: print("Producto"), text="Quiero productos", style="OutlineBlack.TButton").place(x=55, y=607, width=250, height=35)

def mostrar_pantalla_login():
    clear()
    canvas = ttk.Canvas(root, width=360, height=750)
    canvas.pack()

    imagen_login = Image.open("D:/Pasantia/Learny/IMG/Imagen2.png").resize((360, 750))
    bg_img2 = ImageTk.PhotoImage(imagen_login)
    canvas.create_image(0, 0, anchor="nw", image=bg_img2)
    canvas.bg_img = bg_img2

    entry_documento = ttk.Entry(root, font=("Helvetica", 10), bootstyle="")
    entry_documento.insert(0, "Ingrese su documento")
    entry_documento.configure(foreground="gray")
    entry_documento.place(x=20, y=211.5, width=320, height=35)

    def focus_in_doc(e):
        if entry_documento.get() == "Ingrese su documento":
            entry_documento.delete(0, "end")
            entry_documento.configure(foreground="gray")

    def focus_out_doc(e):
        if entry_documento.get() == "":
            entry_documento.insert(0, "Ingrese su documento")
            entry_documento.configure(foreground="white")

    entry_documento.bind("<FocusIn>", focus_in_doc)
    entry_documento.bind("<FocusOut>", focus_out_doc)

    btn_continuar = ttk.Button(
        root,
        text="Iniciar sesión",
        style="secondary.TButton",
        state="disabled",
        command=lambda: mostrar_pantalla_clave(entry_documento.get())
    )
    btn_continuar.place(x=110, y=315, width=140, height=40)

    def verificar_entrada(event):
        cedula = entry_documento.get().strip()
        if cedula in df["Cedula"].values:
            btn_continuar.configure(state="normal", style="DaviviendaRed.TButton")
        else:
            btn_continuar.configure(state="disabled", style="secondary.TButton")

    entry_documento.bind("<KeyRelease>", verificar_entrada)

def mostrar_pantalla_clave(cedula):
    global cliente_activo
    clear()
    canvas = ttk.Canvas(root, width=360, height=750)
    canvas.pack()

    imagen_clave = Image.open("D:/Pasantia/Learny/IMG/Imagen3.png").resize((360, 750))
    bg_img3 = ImageTk.PhotoImage(imagen_clave)
    canvas.create_image(0, 0, anchor="nw", image=bg_img3)
    canvas.bg_img = bg_img3

    entry_clave = ttk.Entry(root, font=("Helvetica", 10), show="", bootstyle="")
    entry_clave.insert(0, "Ingrese su clave")
    entry_clave.configure(foreground="gray")
    entry_clave.place(x=17, y=155.5, width=290, height=35)

    btn_login = ttk.Button(root, text="Iniciar sesión", style="secondary.TButton", state="disabled")
    btn_login.place(x=110, y=270, width=140, height=40)

    def focus_in_clave(e):
        if entry_clave.get() in ["Ingrese su clave", "Clave incorrecta"]:
            entry_clave.delete(0, "end")
            entry_clave.configure(foreground="black", show="*")

    def focus_out_clave(e):
        if entry_clave.get() == "":
            entry_clave.insert(0, "Ingrese su clave")
            entry_clave.configure(foreground="gray", show="")

    def verificar_clave(event):
        clave = entry_clave.get().strip()
        if clave and clave not in ["Ingrese su clave", "Clave incorrecta"]:
            btn_login.configure(state="normal", style="DaviviendaRed.TButton")
        else:
            btn_login.configure(state="disabled", style="secondary.TButton")

    def autenticar():
        clave_ingresada = entry_clave.get().strip()
        cliente = df[df["Cedula"] == cedula]
        if not cliente.empty and clave_ingresada == cliente.iloc[0]["Clave"]:
            cliente_activo = cliente.iloc[0]
            print(f"Bienvenido, {cliente_activo['Nombre']}")
            mostrar_pantalla_principal()
        else:
            entry_clave.delete(0, "end")
            entry_clave.insert(0, "Clave incorrecta")
            entry_clave.configure(foreground="red", show="")
            btn_login.configure(state="disabled", style="secondary.TButton")

    entry_clave.bind("<FocusIn>", focus_in_clave)
    entry_clave.bind("<FocusOut>", focus_out_clave)
    entry_clave.bind("<KeyRelease>", verificar_clave)

    btn_login.configure(command=autenticar)

def mostrar_pantalla_principal():
    clear()
    canvas = ttk.Canvas(root, width=360, height=750)
    canvas.pack()

    imagen_main = Image.open("D:/Pasantia/Learny/IMG/Imagen4.png").resize((360, 750))
    bg_img4 = ImageTk.PhotoImage(imagen_main)
    canvas.create_image(0, 0, anchor="nw", image=bg_img4)
    canvas.bg_img = bg_img4

    # Cargar ícono sin fondo visible
    icono = Image.open("D:/Pasantia/Learny/IMG/Icono.png").resize((60, 60))
    icono_img = ImageTk.PhotoImage(icono)

    # Dibujar directamente sobre el canvas (sin botón)
    canvas.icono_img = icono_img  # evitar garbage collection
    icono_canvas = canvas.create_image(300, 490, anchor="nw", image=icono_img)

    # Crear una zona invisible encima del ícono que actúe como botón
    def on_click(event):
        msg.showinfo("Soporte", "Este botón abrirá el chat de asistencia.")

    canvas.tag_bind(icono_canvas, "<Button-1>", on_click)


# --------------------------
# INICIO
# --------------------------
mostrar_pantalla_inicio()
root.mainloop()
