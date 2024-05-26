import cv2
import numpy as np

img = cv2.imread('schwarz.png')
assert img is not None, "Failed to load image"
img = cv2.resize(img, dsize=None, fx=0.33, fy=0.33, interpolation= cv2.INTER_LINEAR)

img_display = img.copy()

rect_points = []
original_points = []

dragging_point = None

def draw_points_and_lines():
    global img_display
    img_display = img.copy()
    if len(rect_points) > 1:
        for i in range(len(rect_points)-1):
            cv2.line(img_display, rect_points[i], rect_points[i+1], (255, 0, 0), 2)
        cv2.line(img_display, rect_points[-1], rect_points[0], (255, 0, 0), 2)  # Close the loop

    for point in rect_points:
        cv2.circle(img_display, point, 5, (0, 0, 255), -1)

def mouse_events(event, x, y, flags, param):
    global rect_points, dragging_point

    if event == cv2.EVENT_LBUTTONDOWN:
        for idx, pt in enumerate(rect_points):
            if abs(x - pt[0]) < 10 and abs(y - pt[1]) < 10:
                dragging_point = idx
                return

        if len(rect_points) < 4:
            rect_points.append((x, y))
            draw_points_and_lines()

    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging_point is not None:
            rect_points[dragging_point] = (x, y)
            draw_points_and_lines()

    elif event == cv2.EVENT_LBUTTONUP:
        if dragging_point is not None:
            rect_points[dragging_point] = (x, y)
            dragging_point = None
            draw_points_and_lines()

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_events)

points_saved = False

while True:
    cv2.imshow('image', img_display)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

    if not points_saved and len(rect_points) == 4:
        original_points = rect_points.copy()
        print("Original points saved for homography:", original_points)
        points_saved = True

    if key == ord('s') and len(rect_points) == 4:
        original_points = np.array(original_points, dtype=np.float32).reshape(-1, 1, 2)
        rect_points = np.array(rect_points, dtype=np.float32).reshape(-1, 1, 2)

        homography_matrix, _ = cv2.findHomography(srcPoints=original_points, dstPoints=rect_points)
        dsize = (img_display.shape[1], img_display.shape[0])

        warped_image = cv2.warpPerspective(src=img_display, M=homography_matrix, dsize=dsize)
        cv2.destroyAllWindows()

        cv2.imshow('image', warped_image)
        key = cv2.waitKey(1) & 0xFF

cv2.destroyAllWindows()
# https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html
