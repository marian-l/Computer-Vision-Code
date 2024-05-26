import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt, exp

# Function to plot images
def plot_figure(images: list, titles: list, rows: int, columns: int, fig_width=15, fig_height=7):
    fig = plt.figure(figsize=(fig_width, fig_height))
    count = 1
    for image, title in zip(images, titles):
        fig.add_subplot(rows, columns, count)
        count += 1
        plt.imshow(image)
        plt.axis('off')
        plt.title(title)

# Function to compute distance
def distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Gaussian Low-Pass-Filter using sigma
def gaussianLP(sigma, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            base[i, j] = np.exp(-distance((i, j), center) ** 2 / (2 * sigma ** 2))
    return base

# Gaussian High-Pass-Filter using sigma
def gaussianHP(sigma, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for i in range(rows):
        for j in range(cols):
            base[i, j] = 1 - np.exp(-distance((i, j), center) ** 2 / (2 * sigma ** 2))
    return base

# Function to apply FFT, filter and IFFT to each color channel
def process_channel(channel, filter_fn, sigma):
    original = np.fft.fft2(channel)
    center = np.fft.fftshift(original)
    filtered_center = center * filter_fn(sigma, channel.shape)
    filtered = np.fft.ifftshift(filtered_center)
    inverse_filtered = np.fft.ifft2(filtered)
    return np.abs(inverse_filtered)

# Function to generate hybrid image
def main():
    sigma = float(sigmaInput.get())

    resized_1 = cv2.resize(file_1, (500, 500))
    resized_2 = cv2.resize(file_2, (500, 500))

    hybrid_image = np.zeros_like(resized_1)

    for channel in range(3):  # Process each channel separately
        low_pass = process_channel(resized_1[:, :, channel], gaussianLP, sigma)
        high_pass = process_channel(resized_2[:, :, channel], gaussianHP, sigma)
        hybrid_image[:, :, channel] = np.clip(low_pass + high_pass, 0, 255)

    plot_figure([cv2.cvtColor(file_1, cv2.COLOR_BGR2RGB), cv2.cvtColor(file_2, cv2.COLOR_BGR2RGB), cv2.cvtColor(hybrid_image.astype(np.uint8), cv2.COLOR_BGR2RGB)],
                ['A', 'B', 'Hybrid Image'], 1, 3)
    plt.show()

# Set up the GUI
root = tk.Tk()

Label(root, text="Sigma").grid(row=0)

sigmaInput = Entry(root)
sigmaInput.grid(row=0, column=1)

Button_1 = Button(master=root, height=2, width=10, text="Generate", command=main)
Button_1.grid(row=0, column=3)

file_1 = filedialog.askopenfilename(title="Select the first image")
file_2 = filedialog.askopenfilename(title="Select the second image")

file_1 = cv2.imread(file_1)
file_2 = cv2.imread(file_2)

mainloop()
