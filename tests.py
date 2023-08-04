from PIL import Image, ImageDraw, ImageFont

# Crear una imagen en blanco
width, height = 40, 40
image = Image.new('L', (width, height), 255)
draw = ImageDraw.Draw(image)

# Fuente y texto
font_path = f'C:/Windows/fonts/OCRAEXT.TTF'
font_size = 30
text = "R"
font = ImageFont.truetype(font_path, font_size)
width, height = font_size, font_size
image = Image.new('L', (width, height), 255)
draw = ImageDraw.Draw(image)
text_size = draw.textbbox((0, 0), text, font=font)
x = (width - text_size[2] + text_size[0]) // 2
y = (height - text_size[3] - text_size[1]) // 2
draw.text((x, y), text, font=font, fill=0)

# Calcular las coordenadas para centrar el recuadro
x1, y1, x2, y2 = text_size
text_width = x2 - x1
text_height = y2 - y1

# Calcular las coordenadas para centrar el recuadro
x1 = (width - text_width) // 2
y1 = (height - text_height) // 2
x2 = x1 + text_width
y2 = y1 + text_height

# Dibujar la caja delimitadora en la imagen
draw.rectangle((x1, y1, x2, y2), outline=0)


# Mostrar la imagen
image.show()
print(x1, y1, x2, y2)

