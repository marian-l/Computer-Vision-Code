import numpy as np

Image = np.array([[4, 3], [2, 1]])

F = np.fft.fft2(Image)

print('Fourier Transform of Image: ', F)


