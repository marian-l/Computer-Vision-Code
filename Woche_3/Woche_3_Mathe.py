import cv2
import numpy as np
from scipy.signal import correlate2d

Image = np.array([
    [0, 1, 1, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 0, 0]], dtype=np.float32)

Kernel = np.array([[0, 1, 0],
                   [1, 1, 0],
                   [0, 0, 0]], dtype=np.float32)

flipped_Kernel = cv2.flip(Kernel, -1)

result = correlate2d(Image, flipped_Kernel, mode='same', boundary='wrap')

print(result)

# result = cv2.filter2D(src=Image, ddepth=-1, kernel=flipped_Kernel, borderType=cv2.BORDER_WRAP)
# flipped_Kernel = np.flipud(np.fliplr(Kernel))
