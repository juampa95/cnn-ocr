import os
from rectangle_detector import TextRectanglesDetector

# bbox = rec_detect.get_bbox_coor(image)
# if bbox is not None:
#     bbox_path = f'{char_folder}/{c}.bbox.txt'
#     with open(bbox_path, 'w') as bbox_file:
#         bbox_file.write(','.join(str(coord) for coord in bbox))


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


bbox_creator('D:/gitProyects/cnn-ocr/characters')
