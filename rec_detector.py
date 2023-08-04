import cv2 as cv
import matplotlib.pyplot as plt
"""
Creates a rectangle in which the entire character is embedded. 
Giving as output the coordinates of the same, or a representation by image on the screen

Used in conjunction with bbox_creator.py to create bounding boxes
"""


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
        self.margin = 5

    def detect_rectangles(self,image_path,r = 'src'):
        # Leer la imagen de entrada
        src = cv.imread(image_path)

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

        # Fusionar los rectángulos de cada línea de texto
        rectangles = self.merge_rectangles(rectangles)

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
            return rectangles


    def merge_rectangles(self, rectangles):
        rectangles = sorted(rectangles, key=lambda r: (r[1], r[0]))  # Ordenar los rectángulos por coordenada Y y X

        merged_rectangles = []
        current_line = []
        prev_y = None

        for rect in rectangles:
            x, y, w, h = rect

            if prev_y is None or y - prev_y > self.max_line_gap:
                if current_line:
                    merged_rectangles.append(self.merge_line_rectangles(current_line))
                    current_line = []

            current_line.append(rect)
            prev_y = y

        if current_line:
            merged_rectangles.append(self.merge_line_rectangles(current_line))

        return merged_rectangles

    def merge_line_rectangles(self, rectangles):
        min_x = min(rect[0] for rect in rectangles)
        min_y = min(rect[1] for rect in rectangles)
        max_x = max(rect[0] + rect[2] for rect in rectangles)
        max_y = max(rect[1] + rect[3] for rect in rectangles)

        return (min_x, min_y, max_x - min_x, max_y - min_y)

    def show_bbox_image(self, image_path):
        bbox = self.detect_rectangles(image_path)
        plt.imshow(cv.cvtColor(bbox, cv.COLOR_BGR2RGB))
        plt.title('Rectangles Detection')
        plt.show()

    def get_bbox_coor(self, image_path):
        bbox = self.detect_rectangles(image_path, 'bbox')
        return bbox


# image_path = 'characters/A/6n.png'
#
# detector = TextRectanglesDetector()
# detector.show_bbox_image(image_path)
#
# print(detector.get_bbox_coor(image_path))