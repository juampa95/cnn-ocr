import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class TextRectanglesDetector:
    def __init__(self):
        self.threshold = 100
        self.min_area = 10
        self.max_line_gap = 2
        self.min_char_width = 5
        self.max_char_width = 60
        self.min_char_height = 10
        self.max_char_height = 60
        self.min_total_width = 10
        self.max_total_width = 300
        self.min_total_height = 10
        self.max_total_height = 100
        self.margin = 2

    def detect_rectangles(self,image_path,r = 'src'):
        if isinstance(image_path, str):
            src = cv.imread(image_path)
        elif isinstance(image_path, Image.Image):
            src = cv.cvtColor(np.array(image_path), cv.COLOR_RGB2BGR)
        else:
            raise ValueError("El parámetro 'image_input' debe ser una ruta de archivo o un objeto Image de Pillow.")

        # Convertir la imagen a escala de grises y aplicar desenfoque
        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        src_gray = cv.blur(src_gray, (3, 3))

        # Procesar la imagen
        canny_output = cv.Canny(src_gray, self.threshold, self.threshold * 2)
        contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        rectangles = []

        for i, c in enumerate(contours):
            area = cv.contourArea(c)
            if area > self.min_area:
                x, y, w, h = cv.boundingRect(c)

                if self.min_char_width <= w <= self.max_char_width and self.min_char_height <= h <= self.max_char_height:
                    rectangles.append((x, y, w, h))

        filtered_rectangles = []

        for rect in rectangles:
            x, y, w, h = rect
            x -= self.margin
            y -= self.margin
            w += 2 * self.margin
            h += 2 * self.margin

            if self.min_total_width <= w <= self.max_total_width and self.min_total_height <= h <= self.max_total_height:
                filtered_rectangles.append(rect)
                color = (255, 0, 0)
                cv.rectangle(src, (x, y), (x + w, y + h), color, 2)

        if r == 'src':
            return src
        if r == 'bbox':
            return filtered_rectangles

    def show_bbox_image(self, image_path):
        bbox = self.detect_rectangles(image_path)
        plt.imshow(cv.cvtColor(bbox, cv.COLOR_BGR2RGB))
        plt.title('Rectangles Detection')
        plt.show()

    def get_bbox_coor(self, image_path):
        x, y, w, h = None, None, None, None
        bbox = self.detect_rectangles(image_path, 'bbox')
        if bbox:
            x, y, w, h = bbox[0]
        return x, y, w, h

# # Uso de la clase TextRectanglesDetector para una sola imagen
# image_path = 'D:/gitProyects/cnn-ocr/characters/0/4sr.png'
#
# detector = TextRectanglesDetector()
# detector.show_bbox_image(image_path)
#
# print(detector.get_bbox_coor(image_path))