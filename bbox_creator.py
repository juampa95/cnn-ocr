import os
from rectangle_detector import TextRectanglesDetector
"""
Use the TextRectanglesDetector object to creates the coordinates 
of the bbox in the format (x, y, w, h) where:
x = initial x-coordinate
y = initial y-coordinate
w = width of the box
h = height of the box
Create a file with the same name as the image but with the extension '.bbox.txt'
"""


def bbox_creator(path):
    rec_detect = TextRectanglesDetector()
    for char_folder in os.listdir(path):
        char_folder_path = os.path.join(path,char_folder)

        if os.path.isdir(char_folder_path):
            for image_file in os.listdir(char_folder_path):
                if image_file.endswith('.png'):
                    image_path = os.path.join(char_folder_path, image_file)
                    bbox = rec_detect.get_bbox_coor(image_path)
                    bbox_file_name = os.path.splitext(image_file)[0] + '.bbox.txt'
                    bbox_file_path = os.path.join(char_folder_path, bbox_file_name)
                    with open(bbox_file_path, 'w') as bbox_file:
                        bbox_file.write(','.join(str(coord) for coord in bbox))


bbox_creator('characters/')
