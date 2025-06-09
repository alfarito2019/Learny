import tkinter as tk
from tkinter import messagebox
from groq import Groq

def get_ai_response(query):
    client = Groq(api_key="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")  # Reemplaza con tu API real
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres Learny, un asistente conversacional simpático, paciente, y con sentido del humor. Siempre explicas las cosas de forma clara y usas ejemplos sencillos si es posible. Hablas unicamente en español."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def responder_mensaje(mensaje):
    mensaje = mensaje.lower()

    temas_bancarios = ["interés", "intereses", "crédito", "capital", "financiación"]
    
    if any(tema in mensaje for tema in temas_bancarios):
        respuesta = "Claro, puedo ayudarte con temas financieros. ¿Quieres ver una infografía?"
        return {"texto": respuesta, "mostrar_boton": True}
    else:
        respuesta = "Hola, soy Learny, tu asistente bancario. ¿En qué puedo ayudarte hoy?"
        return {"texto": respuesta, "mostrar_boton": False}

def mostrar_chat_ai(parent):
    ventana_chat = tk.Toplevel(parent)
    ventana_chat.title("Chat con Learny")
    ventana_chat.geometry("360x500")
    ventana_chat.configure(bg="#f0f0f0")

    # Marco con scroll
    marco_chat = tk.Canvas(ventana_chat, bg="#f0f0f0", bd=0, highlightthickness=0)
    scrollbar = tk.Scrollbar(ventana_chat, command=marco_chat.yview)
    marco_chat.configure(yscrollcommand=scrollbar.set)

    frame_mensajes = tk.Frame(marco_chat, bg="#f0f0f0")
    marco_chat.create_window((0, 0), window=frame_mensajes, anchor="nw")

    def on_frame_configure(event):
        marco_chat.configure(scrollregion=marco_chat.bbox("all"))

    frame_mensajes.bind("<Configure>", on_frame_configure)

    marco_chat.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Entrada de texto
    entrada = tk.Entry(ventana_chat, font=("Helvetica", 10))
    entrada.pack(fill=tk.X, padx=10, pady=5)
    entrada.focus()

    def mostrar_burbuja(frame, texto, lado="izquierda", bg="white", fg="black"):
        burbuja = tk.Label(
            frame,
            text=texto,
            bg=bg,
            fg=fg,
            wraplength=250,
            justify="left",
            font=("Helvetica", 10),
            padx=10,
            pady=5
        )
        burbuja.pack(anchor="e" if lado == "derecha" else "w", padx=10, pady=5)
        ventana_chat.update_idletasks()
        marco_chat.yview_moveto(1.0)  # Auto-scroll al final

    def enviar():
        mensaje = entrada.get().strip()
        if mensaje == "":
            return
        mostrar_burbuja(frame_mensajes, f"Tú: {mensaje}", lado="derecha", bg="#DCF8C6", fg="black")
        entrada.delete(0, tk.END)
        ventana_chat.update()

        try:
            respuesta = get_ai_response(mensaje)
            mostrar_burbuja(frame_mensajes, f"Learny: {respuesta}", lado="izquierda", bg="white", fg="black")
        except Exception as e:
            mostrar_burbuja(frame_mensajes, "Error al conectar con Learny.", lado="izquierda", bg="red", fg="white")
            print("Error:", e)

    entrada.bind("<Return>", lambda event: enviar())