import shutil
import os

path = "characters/"
path_datasets = "datasets/"

for char_folder in os.listdir(path):
    img_path = os.listdir(path+char_folder)
    os.makedirs(path_datasets+char_folder,exist_ok=True)
    for img in img_path:
        if img.endswith('.png'):
            origen = os.path.join(path, char_folder, img)
            destino = os.path.join(path_datasets, char_folder, img)

            shutil.copy(origen, destino)