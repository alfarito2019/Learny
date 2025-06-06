import tkinter as tk
from tkinter import scrolledtext
from groq import Groq

def getAiResponse(query):
    client = Groq(api_key="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")

    chat_completition = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres Learny, un asistente conversacional simpático, paciente, y con sentido del humor. Siempre explicas las cosas de forma clara y usas ejemplos sencillos si es posible. hablas unicamente en español"+
                "y estás especialmente enfocado en resolver dudas sobre "
            },
            {
                "role": "user",
            "content": query
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completition.choices[0].message.content

# Interfaz gráfica con tkinter
def enviar_mensaje():
    mensaje = entrada.get()
    if mensaje.strip() == "":
        return
    chat.insert(tk.END, f"Tú: {mensaje}\n")
    entrada.delete(0, tk.END)

    respuesta = getAiResponse(mensaje)
    chat.insert(tk.END, f"Learny: {respuesta}\n\n")
    chat.see(tk.END)

# Crear ventana
ventana = tk.Tk()
ventana.title("Chat con Learny")

chat = scrolledtext.ScrolledText(ventana, width=80, height=25, wrap=tk.WORD)
chat.pack(padx=10, pady=10)

entrada = tk.Entry(ventana, width=80)
entrada.pack(padx=10, pady=5)

boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack(pady=5)

ventana.mainloop()