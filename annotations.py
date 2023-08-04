import json
import os
"""
Create a json file for each character that contains the annotations with the path of each 
image and the coordinates of the bbox
"""

def annotations_creator(path):
    for char_folder in os.listdir(path):
        char_folder_path = os.path.join(path, char_folder)
        if os.path.isdir(char_folder_path):
            char_annotations = []

            for image_file in os.listdir(char_folder_path):
                if image_file.endswith('.png'):
                    image_path = (os.path.join(char_folder_path, image_file)).replace('\\', '/')
                    bbox_file = os.path.splitext(image_file)[0] + ".bbox.txt"
                    bbox_path = (os.path.join(char_folder_path, bbox_file)).replace('\\', '/')

                    if os.path.exists(bbox_path):
                        with open(bbox_path, 'r') as f:
                            line = f.readline().strip()
                            if "None" not in line:
                                bbox = [int(val) for val in line.split(',')]

                                annotation = {
                                    "image_path": image_path,
                                    "annotations":
                                        {
                                            "class": char_folder,
                                            "bbox": bbox
                                        }

                                }
                                char_annotations.append(annotation)

                    char_json_path = os.path.join(char_folder_path, f'{char_folder}.json')
                    with open (char_json_path, 'w') as json_file:
                        json.dump(char_annotations, json_file, indent=4)


annotations_creator('characters/')
