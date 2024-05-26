import numpy as np
import scipy as sc
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt, exp


# Windows with 3 Parameters: f1, f2, and sigma


def plot_figure(images: list, titles: list, rows: int, columns: int, fig_width=15, fig_height=7):
    fig = plt.figure(figsize=(fig_width, fig_height))
    count = 1
    for image, title in zip(images, titles):
        fig.add_subplot(rows, columns, count)
        count += 1
        plt.imshow(image, 'gray')
        plt.axis('off')
        plt.title(title)


def distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Gaussian Low-Pass-Filter
def gaussianLP(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            base[i, j] = np.exp(-distance((i, j), center) ** 2 / (2 * D0 ** 2))
    return base


# Function to get high frequency component
# D0 is cutoff frequency
def gaussianHP(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            base[i, j] = 1 - np.exp(-distance((i, j), center) ** 2 / (2 * D0 ** 2))
    return base


# Function to generate hybrid image
# D0 is cutoff frequency

def main():
    # Resize both images to 128x128 to avoid different image size issue
    sigma = sigmaInput.get()

    resized_gray_1 = cv2.resize(gray_file_1, (128, 128))
    resized_gray_2 = cv2.resize(gray_file_2, (128, 128))

    original1 = np.fft.fft2(resized_gray_1)  # Get the fourier of image1
    center1 = np.fft.fftshift(original1)  # Apply Centre shifting
    LowPassCenter = center1 * gaussianLP(int(sigma), resized_gray_1.shape)  # Extract low frequency component
    LowPass = np.fft.ifftshift(LowPassCenter)
    inv_LowPass = np.fft.ifft2(LowPass)  # Get image using Inverse FFT

    original2 = np.fft.fft2(resized_gray_2)
    center2 = np.fft.fftshift(original2)
    HighPassCenter = center2 * gaussianHP(int(sigma), resized_gray_2.shape)  # Extract high frequency component
    HighPass = np.fft.ifftshift(HighPassCenter)
    inv_HighPass = np.fft.ifft2(HighPass)
    result = np.abs(inv_LowPass) + np.abs(inv_HighPass)  # Generate the hybrid image

    plot_figure([file_1, file_2, result], ['A', 'B', 'Hybrid Image'], 1, 3)
    plt.show()


root = tk.Tk()

Label(root, text="Sigma").grid(row=0)
Label(root, text="Calculate").grid(row=0, column=2)

sigmaInput = Entry(root)
sigmaInput.grid(row=0, column=1)

Button_1 = Button(master=root, height=10, width=20, command=main)
Button_1.grid(row=0, column=3)

file_1 = filedialog.askopenfilename()
file_2 = filedialog.askopenfilename()

file_1 = cv2.imread(file_1)
file_2 = cv2.imread(file_2)

gray_file_1 = cv2.cvtColor(file_1, cv2.COLOR_BGR2GRAY)
gray_file_2 = cv2.cvtColor(file_2, cv2.COLOR_BGR2GRAY)

mainloop()
# https://www.geeksforgeeks.org/creating-hybrid-images-using-opencv-library-python/