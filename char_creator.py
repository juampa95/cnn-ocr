import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
"""
Creates an image of the characters given as input parameters in the selected font. 
Additionally, it creates distorted images of this same character (size, deformations, noise, etc).

The images are organized within the 'base_folder' within folders that are automatically created 
with the name of each character.
"""

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

                    # Create different sizes of each char
                    font = ImageFont.truetype(font_path, font_size)
                    width, height = font_size, font_size
                    image = Image.new('L', (width, height), background_color)
                    draw = ImageDraw.Draw(image)
                    text_size = draw.textbbox((0, 0), char, font=font)
                    x = (width - text_size[2] + text_size[0]) // 2
                    y = (height - text_size[3] - text_size[1]) // 2
                    draw.text((x, y), char, font=font, fill=text_color)
                    image.save(f'{char_folder}/{c}.png')

                    # Do noise random for each char
                    imageNoise = add_noise(image)
                    imageNoise.save(f'{char_folder}/{c}n.png')

                    # Do deformation for each char (left shearing)
                    imageShearingl = def_img_shearing(image, 0.2)
                    imageShearingl.save(f'{char_folder}/{c}sl.png')

                    # Do deformation for each char (right shearing)
                    imageShearingr = def_img_shearing(image, -0.2)
                    imageShearingr.save(f'{char_folder}/{c}sr.png')

                    # Do two rotation for each char
                    imageRotation = def_img_rotation(image, font_size, 15)
                    imageRotation.save(f'{char_folder}/{c}r+.png')
                    imageRotation = def_img_rotation(image, font_size, -15)
                    imageRotation.save(f'{char_folder}/{c}r-.png')
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


def def_img_shearing(image, shear_x):
    image_array = np.array(image)
    deformation_matrix = np.array([[1, shear_x, 0], [0, 1, 0]], dtype=float)
    deformed_image = cv2.warpAffine(image_array, deformation_matrix, image_array.shape[::-1], borderMode=cv2.BORDER_CONSTANT, borderValue=255)
    return Image.fromarray(deformed_image)


def def_img_rotation(image, img_size, angle):
    image_array = np.array(image)
    deformation_matrix = cv2.getRotationMatrix2D((img_size / 2, img_size / 2), angle, 1)
    deformed_image = cv2.warpAffine(image_array, deformation_matrix, image_array.shape[::-1], borderMode=cv2.BORDER_CONSTANT, borderValue=255)
    return Image.fromarray(deformed_image)


def def_img_scaling(image):
    image_array = np.array(image)
    scale_x = 1.5
    scale_y = 1.5
    deformation_matrix = np.array([[scale_x, 0, 0], [0, scale_y, 0]], dtype=float)
    deformed_image = cv2.warpAffine(image_array, deformation_matrix, image_array.shape[::-1], borderMode=cv2.BORDER_CONSTANT, borderValue=255)
    return Image.fromarray(deformed_image)


char_list = f'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
create_char('OCRAEXT', char_list, 'D:/gitProyects/cnn-ocr/characters')
