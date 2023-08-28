from PIL import Image, ImageDraw, ImageFont



# Definir el texto y la fuente
lines = ["NS: SYIVB983MGFRXC1", "V: 17/03/2045", "L: ZRPLKX549800OUS", "E: 02/07/2084"]
font_path = "C:/WINDOWS/FONTS/OCRAEXT.TTF"  # Ruta a tu fuente
font_size = 40
name = "img6"

# Alto y ancho de imagen en funcion de cantidad de caracteres y lineas de texto
height = font_size*(len(lines))+40
x = 0
for line in lines:
    if len(line) > x:
        x = len(line)
        print(x)

width = int(font_size*6/10)*x + font_size

# width, height = 600, 200
image = Image.new("L", (width, height), 255)
draw = ImageDraw.Draw(image)

# Cargar la fuente
font = ImageFont.truetype(font_path, font_size)

# Coordenadas iniciales para el primer carácter
x, y = 10, 10

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
image.save(name+".png")

# Crear un archivo de texto con la información de las bounding boxes
with open(name+".txt", "w") as file:
    for info in bounding_boxes_info:
        char, x1, y1, x2, y2 = info
        file.write(f"{char} {x1} {y1} {x2} {y2}\n")

# Mostrar la imagen
image.show()



# Abrir la imagen original sin los bounding boxes
image = Image.open(name+".png")

# Cargar la información de las bounding boxes desde el archivo de texto
bounding_boxes_info = []
with open(name+".txt", "r") as file:
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
