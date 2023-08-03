import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont


def create_char(font_name, char_list, base_folder):
    font_path = f'C:/Windows/fonts/{font_name}.ttf'
    background_color = 255
    text_color = 0
    font_sizes = [25, 30, 40, 50, 60, 70, 80]

    if os.path.exists(font_path):
        if os.path.exists(base_folder):

            for char in char_list:
                char_folder = os.path.join(base_folder, char)

                if not os.path.exists(char_folder):
                    os.makedirs(char_folder)
                c = 0
                for font_size in font_sizes:
                    font = ImageFont.truetype(font_path, font_size)
                    width, height = font_size, font_size
                    image = Image.new('L', (width, height), background_color)
                    draw = ImageDraw.Draw(image)
                    text_size = draw.textbbox((0, 0), char, font=font)
                    x = (width - text_size[2] + text_size[0]) // 2
                    y = (height - text_size[3] - text_size[1]) // 2
                    draw.text((x, y), char, font=font, fill=text_color)
                    image.save(f'{char_folder}/{c}.png')
                    c += 1
        else:
            print('El directorio base seleccionado para crear la salida no existe.')
    else:
        print('La fuente seleccionada no existe, verificar que el nombre y la ruta sea correcta.')


def add_noise(image, noise_type='salt_and_pepper', magnitude=0.05):
    image_array = np.array(image)  # Convierte la imagen a un arreglo NumPy
    if noise_type == 'gaussian':
        noise = np.random.normal(scale=magnitude, size=image_array.shape)
    elif noise_type == 'salt_and_pepper':
        noise = np.random.choice([0, 200], size=image_array.shape, p=[1 - magnitude, magnitude])
    noisy_image = np.clip(image_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)



create_char('OCRAEXT', 'ABC8', 'D:/gitProyects/cnn-ocr/characters')

image_path = 'D:/gitProyects/cnn-ocr/characters/8/5.png'
image = Image.open(image_path)

noisy_image = add_noise(image)
noisy_image.show()