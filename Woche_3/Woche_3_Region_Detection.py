import cv2
import numpy as np
from matplotlib import pyplot as plt

# https://stackoverflow.com/questions/28340950/opencv-how-to-draw-continously-with-a-mouse | Abhishek Kumar
drawing = False  # true if mouse is pressed
pt1_x, pt1_y = None, None

template = None

# Mouse callback function to draw a rectangle
def line_drawing(event, x, y, flags, param):
    global pt1_x, pt1_y, drawing, template, img_rgb
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        top_left = (min(pt1_x, x), min(pt1_y, y))
        bottom_right = (max(pt1_x, x), max(pt1_y, y))
        cv2.rectangle(img_rgb, top_left, bottom_right, (0, 255, 0), 2)
        template = img_gray[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        if template.size != 0:
            cv2.imshow('template', template)

img_rgb = cv2.imread('koreanSigns.png')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('image')
cv2.setMouseCallback('image', line_drawing)

while True:
    cv2.imshow('image', img_rgb)
    key = cv2.waitKey(1) & 0xFF

    if template is not None:
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imwrite('res.png', img_rgb)

cv2.destroyAllWindows()
