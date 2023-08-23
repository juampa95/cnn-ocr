from PIL import Image, ImageDraw, ImageFont

# Crear una imagen en blanco en modo RGB
width, height = 500, 220
image = Image.new("L", (width, height), 255)
draw = ImageDraw.Draw(image)

# Definir el texto y la fuente
lines = ["NS: 12344567892", "V: 02/08/2025", "L: AXU023671", "E: 08/10/2023"]
font_path = "C:/WINDOWS/FONTS/OCRAEXT.TTF"  # Ruta a tu fuente
font_size = 40

# Cargar la fuente
font = ImageFont.truetype(font_path, font_size)

# Coordenadas iniciales para el primer carácter
x, y = 20, 20

# Espacio entre líneas
line_spacing = 10

# Margen alrededor de cada letra
margin = 2

# Lista para almacenar la información de las bounding boxes
bounding_boxes_info = []

# Dibujar cada letra en cada línea de texto
for line in lines:
    for char in line:
        if char not in [" "]:
            # Obtener el tamaño del carácter
            char_width, char_height = draw.textbbox((0, 0), char, font=font, align="left")[2:]

            # Calcular la nueva posición x con margen
            new_x = x + margin

            # Dibujar el rectángulo de la bounding box directamente alrededor del carácter
            bbox = (
                new_x + margin,
                y + 2 * margin,
                new_x + char_width - margin,
                y + char_height + margin
            )

            # Almacenar la información de la bounding box en la lista
            bounding_boxes_info.append((char, bbox[0], bbox[1], bbox[2], bbox[3]))

        # Dibujar el carácter en la imagen usando la nueva posición x
        draw.text((new_x, y), char, fill="black", font=font)

        # Actualizar la coordenada x para el próximo carácter
        x += char_width

    # Restaurar la coordenada x y actualizar la coordenada y para la próxima línea
    x = 20
    y += char_height + line_spacing

# Guardar la imagen sin los bounding boxes
image.save("output_image.png")

# Crear un archivo de texto con la información de las bounding boxes
with open("bounding_boxes.txt", "w") as file:
    for info in bounding_boxes_info:
        char, x1, y1, x2, y2 = info
        file.write(f"{char} {x1} {y1} {x2} {y2}\n")

# Mostrar la imagen
image.show()



# Abrir la imagen original sin los bounding boxes
image = Image.open("output_image.png")

# Cargar la información de las bounding boxes desde el archivo de texto
bounding_boxes_info = []
with open("bounding_boxes.txt", "r") as file:
    for line in file:
        char, x1, y1, x2, y2 = line.strip().split()
        bounding_boxes_info.append((char, int(x1), int(y1), int(x2), int(y2)))

# Crear un objeto ImageDraw para dibujar en la imagen
draw = ImageDraw.Draw(image)

# Dibujar los bounding boxes en la imagen
for info in bounding_boxes_info:
    char, x1, y1, x2, y2 = info
    draw.rectangle([(x1, y1), (x2, y2)], outline="red")

# Mostrar la imagen
image.show()
