import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import pandas as pd
import tkinter.messagebox as msg
import tkinter as tk

# --------------------------
# BASE DE DATOS Y VARIABLES
# --------------------------
bd_path = "./BD.xlsx"
df = pd.read_excel(bd_path)
df["Cedula"] = df["Cedula"].astype(str).str.replace(".0", "", regex=False)
df["Clave"] = df["Clave"].astype(str).str.replace(".0", "", regex=False)

cliente_activo = None

# --------------------------
# ROOT
# --------------------------
root = ttk.Window(themename="flatly")
root.geometry("360x750")
root.resizable(False, False)

# --------------------------
# ESTILOS
# --------------------------
style = ttk.Style()
style.configure("DaviviendaRed.TButton", background="#E0111B", foreground="white",
                font=("Helvetica", 10, "bold"), borderwidth=0)
style.map("DaviviendaRed.TButton",
          background=[("active", "#C50F17")],
          foreground=[("disabled", "#cccccc")])

style.configure("OutlineBlack.TButton", background="white", foreground="black",
                bordercolor="black", relief="solid", borderwidth=2, font=("Helvetica", 10))
style.map("OutlineBlack.TButton",
          background=[("active", "#f0f0f0")],
          foreground=[("active", "black")])

# --------------------------
# UTILIDAD
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

    fondo_inicio = Image.open("./IMG/fondo1.png").resize((361, 465))
    bg_img = ImageTk.PhotoImage(fondo_inicio)
    canvas.create_image(0, 0, anchor="nw", image=bg_img)
    canvas.bg_img = bg_img

    logo = Image.open("./IMG/logodav.png").resize((40, 34))
    logo_img = ImageTk.PhotoImage(logo)
    canvas.create_image(20, 20, anchor="nw", image=logo_img)
    canvas.logo_img = logo_img

    canvas.create_text(20, 60, text="Nos alegra tenerle aquí", anchor="nw", fill="white",
                       font=("Helvetica Neue LT Condensed", 12, "bold"))
    canvas.create_text(20, 90, text="En esta app puede hacerlo todo sin salir de casa. ¿Ya es nuestro cliente?",
                       anchor="nw", fill="white", font=("Helvetica Neue LT Condensed", 8), width=320)

    ttk.Button(root, command=mostrar_pantalla_documento, text="Soy cliente",
               style="DaviviendaRed.TButton").place(x=80, y=562, width=200, height=33)
    ttk.Button(root, command=lambda: print("Producto"), text="Quiero productos",
               style="OutlineBlack.TButton").place(x=80, y=605, width=200, height=35)

def mostrar_pantalla_documento():
    clear()
    canvas = ttk.Canvas(root, width=360, height=750, background="#EBECF0")
    canvas.pack()

    banner = Image.open("./IMG/Inicio.png").resize((360, 73))
    banner_img = ImageTk.PhotoImage(banner)
    canvas.create_image(0, 0, anchor="nw", image=banner_img)
    canvas.banner_img = banner_img

    ttk.Label(root, text="Seleccione el tipo de documento", background="#EBECF0",
              font=("Helvetica", 10)).place(x=30, y=140)
    tipo_doc = ttk.Combobox(root, values=["Cédula de ciudadanía", "Tarjeta de identidad", "Cédula de extranjería"],
                            font=("Helvetica", 10), state="readonly")
    tipo_doc.current(0)
    tipo_doc.place(x=30, y=165, width=300, height=30)

    ttk.Label(root, text="Ingrese el número de documento", background="#EBECF0",
              font=("Helvetica", 10)).place(x=30, y=210)
    entry_documento = ttk.Entry(root, font=("Helvetica", 12))
    entry_documento.place(x=30, y=235, width=300, height=35)

    canvas.create_text(180, 285, text="¿Olvidó o bloqueó su clave virtual?", font=("Helvetica", 9, "bold"),
                       fill="black", anchor="center")

    btn_iniciar = ttk.Button(root, text="Iniciar sesión", style="secondary.TButton", state="disabled",
                             command=lambda: mostrar_pantalla_clave(entry_documento.get()))
    btn_iniciar.place(x=110, y=320, width=140, height=40)

    def verificar_entrada(event):
        cedula = entry_documento.get().strip()
        if cedula in df["Cedula"].values:
            btn_iniciar.configure(state="normal", style="DaviviendaRed.TButton")
        else:
            btn_iniciar.configure(state="disabled", style="secondary.TButton")

    entry_documento.bind("<KeyRelease>", verificar_entrada)

def mostrar_pantalla_clave(cedula):
    global cliente_activo
    clear()
    canvas = ttk.Canvas(root, width=360, height=750, background="#EBECF0")
    canvas.pack()

    banner = Image.open("./IMG/Inicio.png").resize((360, 73))
    banner_img = ImageTk.PhotoImage(banner)
    canvas.create_image(0, 0, anchor="nw", image=banner_img)
    canvas.banner_img = banner_img

    ttk.Label(root, text="Ingrese su clave virtual", background="#EBECF0", font=("Helvetica", 10)).place(x=30, y=140)

    entry_clave = ttk.Entry(root, font=("Helvetica", 12), show="", foreground="gray")
    entry_clave.insert(0, "Clave virtual")
    entry_clave.place(x=30, y=165, width=300, height=35)

    btn_login = ttk.Button(root, text="Iniciar sesión", style="secondary.TButton", state="disabled")
    btn_login.place(x=110, y=270, width=140, height=40)

    canvas.create_text(180, 220, text="¿Olvidó o bloqueó su clave virtual?", font=("Helvetica", 9, "bold"),
                       fill="black", anchor="center")
    canvas.create_text(180, 325, text="Términos y condiciones", font=("Helvetica", 8), fill="gray", anchor="center")

    def focus_in_clave(e):
        if entry_clave.get() in ["Clave virtual", "Clave incorrecta"]:
            entry_clave.delete(0, "end")
            entry_clave.configure(foreground="black", show="*")

    def focus_out_clave(e):
        if entry_clave.get() == "":
            entry_clave.insert(0, "Clave virtual")
            entry_clave.configure(foreground="gray", show="")

    def verificar_clave(event):
        clave = entry_clave.get().strip()
        if clave and clave not in ["Clave virtual", "Clave incorrecta"]:
            btn_login.configure(state="normal", style="DaviviendaRed.TButton")
        else:
            btn_login.configure(state="disabled", style="secondary.TButton")

    def autenticar():
        global cliente_activo
        clave_ingresada = entry_clave.get().strip()
        cliente = df[df["Cedula"] == cedula]
        if not cliente.empty and clave_ingresada == cliente.iloc[0]["Clave"]:
            cliente_activo = cliente.iloc[0]
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

    main_canvas = tk.Canvas(root, width=360, height=750, bg="#EBECF0", highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    frame = ttk.Frame(main_canvas, style="TFrame")

    frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
    main_canvas.create_window((0, 0), window=frame, anchor="nw")
    main_canvas.configure(yscrollcommand=scrollbar.set)

    main_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    banner_canvas = tk.Canvas(frame, width=360, height=73, highlightthickness=0)
    banner_canvas.pack()
    banner = Image.open("./IMG/inicio2.jpg").resize((360, 73))
    banner_img = ImageTk.PhotoImage(banner)
    banner_canvas.create_image(0, 0, anchor="nw", image=banner_img)
    banner_canvas.image = banner_img

    nombre = "USUARIO"
    if cliente_activo is not None:
        try:
            nombre = cliente_activo["Nombre"].split()[0].upper()
        except:
            pass

    banner_canvas.create_text(180, 36, text=f"Hola, {nombre}", font=("Helvetica", 10, "bold"),
                              fill="white", anchor="center")

    ttk.Label(frame, text="Novedades", font=("Helvetica", 10, "bold"), background="#EBECF0").pack(padx=20, anchor="w")
    novedades_img = ImageTk.PhotoImage(Image.open("./IMG/Blan1.jpg").resize((314, 130)))
    ttk.Label(frame, image=novedades_img, background="#EBECF0").pack(padx=20, pady=5)
    frame.novedades_img = novedades_img

    ttk.Label(frame, text="Mis productos", font=("Helvetica", 10, "bold"), background="#EBECF0").pack(padx=20, anchor="w")

    productos_canvas = tk.Canvas(frame, width=340, height=140, bg="#EBECF0", highlightthickness=0)
    productos_frame = ttk.Frame(productos_canvas)
    productos_scroll = ttk.Scrollbar(frame, orient="horizontal", command=productos_canvas.xview)
    productos_canvas.configure(xscrollcommand=productos_scroll.set)

    productos_canvas.create_window((0, 0), window=productos_frame, anchor="nw")
    productos_frame.bind("<Configure>", lambda e: productos_canvas.configure(scrollregion=productos_canvas.bbox("all")))

    productos_canvas.pack(padx=10)
    productos_scroll.pack(padx=10, fill="x")

    for img_path in ["Cuenta.jpg", "Tarjetas.jpg", "Creditos.jpg"]:
        img = ImageTk.PhotoImage(Image.open(f"./IMG/{img_path}").resize((218, 129)))
        lbl = ttk.Label(productos_frame, image=img, style="TLabel")
        lbl.image = img
        lbl.pack(side="left", padx=5)

    ttk.Label(frame, text="Servicios destacados", font=("Helvetica", 11, "bold"),
              background="#EBECF0").pack(padx=20, pady=(10, 0), anchor="w")
    blan2_img = ImageTk.PhotoImage(Image.open("./IMG/blan2.jpg").resize((314, 198)))
    ttk.Label(frame, image=blan2_img, background="#EBECF0").pack(padx=20, pady=5)
    frame.blan2_img = blan2_img

    icono = Image.open("./IMG/Icono.png").resize((50, 50))
    icono_img = ImageTk.PhotoImage(icono)
    btn_icono = tk.Label(root, image=icono_img, bg="#EBECF0", cursor="hand2")
    btn_icono.image = icono_img
    btn_icono.place(x=305, y=440, width=50, height=50)
    btn_icono.bind("<Button-1>", lambda e: mostrar_chat())

# --------------------------
# CHAT
# --------------------------
def mostrar_chat():
    clear()

    # Canvas para encabezado con imagen
    header = tk.Canvas(root, width=360, height=73, highlightthickness=0)
    header.pack()

    banner = Image.open("./IMG/inicio2.jpg").resize((360, 73))
    banner_img = ImageTk.PhotoImage(banner)
    header.create_image(0, 0, anchor="nw", image=banner_img)
    header.image = banner_img

    nombre = "USUARIO"
    if cliente_activo is not None:
        try:
            nombre = cliente_activo["Nombre"].split()[0].upper()
        except:
            pass

    header.create_text(180, 36, text=f"Hola, {nombre}", font=("Helvetica", 10, "bold"),
                       fill="white", anchor="center")

    # Cuerpo del chat
    chat_frame = tk.Frame(root, bg="white")
    chat_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(chat_frame, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
    mensajes_frame = tk.Frame(canvas, bg="white")

    mensajes_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=mensajes_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    input_frame = tk.Frame(root, bg="white")
    input_frame.pack(fill="x", padx=10, pady=5)

    entry_msg = ttk.Entry(input_frame, font=("Helvetica", 10))
    entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def agregar_mensaje_bot(texto):
        burbuja = tk.Label(mensajes_frame, text=texto, bg="white", wraplength=250,
                           justify="left", anchor="w", font=("Helvetica", 10), padx=10, pady=5,
                           bd=1, relief="solid")
        burbuja.pack(anchor="w", padx=10, pady=4)

    def agregar_mensaje_usuario(texto):
        burbuja = tk.Label(mensajes_frame, text=texto, bg="#E5EFFB", wraplength=250,
                           justify="left", anchor="e", font=("Helvetica", 10), padx=10, pady=5,
                           bd=1, relief="solid")
        burbuja.pack(anchor="e", padx=10, pady=4)

    def enviar_mensaje(event=None):
        mensaje = entry_msg.get().strip()
        if mensaje == "":
            return
        agregar_mensaje_usuario(mensaje)
        entry_msg.delete(0, "end")
        root.after(500, lambda: agregar_mensaje_bot("Buenos días. Bienvenido a Davivienda ¿en qué puedo ayudarle?"))

    entry_msg.bind("<Return>", enviar_mensaje)
    btn_enviar = ttk.Button(input_frame, text="➤", command=enviar_mensaje)
    btn_enviar.pack(side="right")

    agregar_mensaje_bot(f"Buenos días señor {nombre.capitalize()}. Bienvenido a Davivienda ¿en qué puedo ayudarle?")

# --------------------------
# INICIO
# --------------------------
mostrar_pantalla_inicio()
root.mainloop()
