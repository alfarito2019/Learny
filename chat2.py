import tkinter as tk
from groq import Groq
import subprocess

# Configura tu clave de API de Groq
client = Groq(api_key="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")  # <-- Pega tu API Key de Groq aquí

# Palabras clave para detectar temas bancarios
PALABRAS_CLAVE = ["interés", "intereses", "crédito", "capital", "cuota", "financiación", "financiamiento", "deuda", "plazo"]


cedula_usuario = None

def set_cedula(cedula):
    global cedula_usuario
    cedula_usuario = cedula

def contiene_tema_relevante(texto):
    texto = texto.lower()
    return any(palabra in texto for palabra in PALABRAS_CLAVE)

# def responder_mensaje(mensaje_usuario):
#     try:
#         respuesta = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "Eres un asesor bancario experto. Tu objetivo es ayudar a los usuarios con dudas relacionadas con productos financieros, tasas de interés, créditos, simulaciones, inversiones y educación financiera. Responde de forma clara, amigable y profesional."
#                 },
#                 {
#                     "role": "user",
#                     "content": pregunta
#                 }
#             ]
#         )
#         respuesta_texto = respuesta.choices[0].message.content.strip()
#     except Exception as e:
#         respuesta_texto = f"Lo siento, ocurrió un error: {e}"

def enviar_mensaje():
    
    pregunta = entry_usuario.get().strip()
    if pregunta == "":
        return

    entry_usuario.delete(0, tk.END)
    caja_texto.config(state="normal")
    caja_texto.insert(tk.END, f"🧑 Tú: {pregunta}\n")
    caja_texto.config(state="disabled")

    # Palabras clave financieras
    palabras_clave = ["interés", "intereses", "crédito", "créditos", "capital", "cuota", "cuotas"]
    mensaje_tiene_palabras_clave = any(palabra in pregunta.lower() for palabra in palabras_clave)

    try:
        # Llamada a Groq con rol de asesor bancario
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asesor bancario experto llamado Vivi. Tu objetivo es ayudar a los usuarios con dudas relacionadas con productos financieros, tasas de interés, créditos, simulaciones, inversiones y educación financiera. Responde de forma clara, amigable y profesional. En el primer mensaje preséntate como Hola soy Vivi, un asistente de Davivienda, ¿En qué puedo ayudarte hoy?"
                },
                {
                    "role": "user",
                    "content": pregunta
                }
            ]
        )

        # Si hay palabras clave, da una respuesta más corta
        if mensaje_tiene_palabras_clave:
            respuesta_texto = "📊 Tengo un contenido para ti sobre este tema."
        else:
            respuesta_texto = respuesta.choices[0].message.content.strip()

    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error: {e}"

    # Mostrar la respuesta del asistente
    caja_texto.config(state="normal")
    caja_texto.insert(tk.END, f"🤖 Vivi: {respuesta_texto}\n")
    caja_texto.config(state="disabled")
    caja_texto.see(tk.END)

    # Mostrar botón justo debajo del mensaje si aplica
    if mensaje_tiene_palabras_clave:
        frame_boton = tk.Frame(caja_texto, bg="#F0F0F0")  # Fondo para que se vea mejor
        boton_infografia = tk.Button(frame_boton, text="📥 Generar Infografía", command=generar_infografia)
        boton_infografia.pack(pady=2)
        caja_texto.window_create(tk.END, window=frame_boton)
        caja_texto.insert(tk.END, "\n")
        caja_texto.see(tk.END)

def generar_infografia():
    subprocess.run(["python", "imagen.py",cedula_usuario])

def mostrar_chat_ai(root):
    global caja_texto, entry_usuario, boton_infografia

    ventana_chat = tk.Toplevel(root)
    ventana_chat.title("Asistente Bancario")
    ventana_chat.geometry("360x500")
    ventana_chat.resizable(False, False)

    caja_texto = tk.Text(ventana_chat, wrap="word", state="disabled", font=("Helvetica", 10), bg="#f8f8f8")
    caja_texto.pack(expand=True, fill="both", padx=10, pady=10)

    frame_entry = tk.Frame(ventana_chat)
    frame_entry.pack(fill="x", padx=10, pady=(0, 10))

    entry_usuario = tk.Entry(frame_entry, font=("Helvetica", 10))
    entry_usuario.pack(side="left", expand=True, fill="x", padx=(0, 10))
    entry_usuario.bind("<Return>", lambda event: enviar_mensaje())

    boton_enviar = tk.Button(frame_entry, text="Enviar", command=enviar_mensaje, bg="#E0111B", fg="white")
    boton_enviar.pack(side="right")

    # Botón para generar infografía (oculto por defecto)
    boton_infografia = tk.Button(ventana_chat, text="Generar Infografía", command=generar_infografia, bg="#0d6efd", fg="white")
    boton_infografia.pack_forget()