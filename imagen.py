import cv2
import os
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image, ImageDraw, ImageFont

# Ruta de Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def analyze_and_replace_text(input_image_path, output_image_path, texts_to_replace, new_texts, text_styles):
    # Leer la imagen de entrada
    image = cv2.imread(input_image_path)

    if image is None:
        print("Error al abrir la imagen.")
        return

    # Convertir la imagen a escala de grises para mejorar la detección de texto
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectar texto en la imagen usando Tesseract
    data = pytesseract.image_to_data(gray_image, output_type=Output.DICT)

    # Crear una máscara para el inpainting
    mask = np.zeros(gray_image.shape, dtype=np.uint8)

    for text_to_replace, new_text in zip(texts_to_replace, new_texts):
        for i in range(len(data['text'])):
            detected_text = data['text'][i].strip()

            if detected_text and text_to_replace in detected_text:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                mask[y:y + h, x:x + w] = 255
                print(f'Texto "{text_to_replace}" encontrado y marcado para reemplazo en la imagen.')

    modified_image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

    pil_image = Image.fromarray(cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)

    for text_to_replace, new_text, style in zip(texts_to_replace, new_texts, text_styles):
        for i in range(len(data['text'])):
            detected_text = data['text'][i].strip()

            if detected_text and text_to_replace in detected_text:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                # Ajustar el tamaño de la fuente
                font_size = h  # Establecer el tamaño de la fuente según la altura del texto detectado
                font = ImageFont.truetype(style['font_path'], font_size)

                # Obtener el tamaño del texto
                bbox = draw.textbbox((0, 0), new_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Calcular la posición del texto centrado
                text_x = x + (w - text_width) // 2
                text_y = y + (h - text_height) // 2

                # Dibujar el texto en la imagen
                draw.text((text_x, text_y), new_text, font=font, fill=style['color'])
                print(
                    f'Texto "{text_to_replace}" reemplazado por "{new_text}" en la imagen en la posición {(text_x, text_y)}.')

    modified_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_image_path, modified_image)
    cv2.namedWindow('Modified Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Modified Image', modified_image)
    cv2.resizeWindow('Modified Image', modified_image.shape[1], modified_image.shape[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Rutas de la imagen de entrada y salida
input_image_path = 'Learny-master\IMAGENES\Infografia.jpg'

output_image_path = 'Learny-master\IMAGENES\Infografia2.jpg'

print("¿Existe la imagen?", os.path.exists(input_image_path))
# Texto a buscar y reemplazar
texts_to_replace = ['Hola', 'Carlos', '17%']
new_texts = ['Buenas tardes', 'Pedro', '35%']

# Estilos de texto personalizados
text_styles = [
    {'font_path': 'arial.ttf', 'color': (0, 0, 0)},  # Negro
    {'font_path': 'arial.ttf', 'color': (0, 0, 255)},  # Rojo
    {'font_path': 'arial.ttf', 'color': (0, 255, 0)},  # Verde
    {'font_path': 'arial.ttf', 'color': (255, 0, 0)}  # Azul
]

analyze_and_replace_text(input_image_path, output_image_path, texts_to_replace, new_texts, text_styles)
