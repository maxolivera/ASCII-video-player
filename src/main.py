from cv2.typing import Size
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
import logging

# image


# Read the image
image = cv2.imread("media/julian.webp", cv2.IMREAD_COLOR)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Target console dimensions
CONSOLE_WIDTH = 180
CONSOLE_HEIGHT = 101

# Resize image to fit console dimensions
aspect_ratio = gray_image.shape[1] / gray_image.shape[0]
new_width = CONSOLE_WIDTH
new_height = int(CONSOLE_WIDTH / (2 *aspect_ratio))
if new_height > CONSOLE_HEIGHT:
    new_height = CONSOLE_HEIGHT
    new_width = int(CONSOLE_HEIGHT * aspect_ratio * 2)

resized_image = cv2.resize(
    gray_image, (new_width, new_height), interpolation=cv2.INTER_AREA
)

# Apply Gaussian Blur twih two different kernel sizes
blur1 = cv2.GaussianBlur(resized_image, (5, 5), 0)
blur2 = cv2.GaussianBlur(resized_image, (9, 9), 0)

# Calculate the Differente of Gaussians
dog = cv2.subtract(blur1, blur2)

# Compue gradients along x and y directions using the Scharr operator
threshold_value = 1.75  # Adjust this value as needed
_, thresholded_dog = cv2.threshold(dog, threshold_value, 255, cv2.THRESH_BINARY)

grad_x = np.nan_to_num(cv2.Scharr(thresholded_dog, cv2.CV_64F, 1, 0))
grad_y = np.nan_to_num(cv2.Scharr(thresholded_dog, cv2.CV_64F, 0, 1))

# cv2.imshow("resized image", cv2.addWeighted(cv2.convertScaleAbs(grad_x), 0.5, cv2.convertScaleAbs(grad_y), 0.5, 0))
# cv2.waitKey(0)
# Compute the gradient magnitud and angle
magnitude = np.sqrt(grad_x**2 + grad_y**2)
angle = np.arctan2(grad_y, grad_x) * (180 / np.pi)

# Normalize the angle to be between 0 and 360 degrees
angle = np.mod(angle + 360, 360)

# ASCII chars
edge_chars = {
    (337.5, 360): '-',
    (0, 22.5): '-',    # Horizontal line at near 0 or 360 degrees
    (22.5, 67.5): '/', # 45 degrees (positive diagonal)
    (67.5, 112.5): '|',# Vertical line
    (112.5, 157.5): '\\',# 135 degrees (negative diagonal)
    (157.5, 202.5): '-',# Horizontal line
    (202.5, 247.5): '/',# Negative diagonal
    (247.5, 292.5): '|',# Vertical line
    (292.5, 337.5): '\\'# Positive diagonal
}

luminance_char = " .:icoO?#■"

# Normalize the magnitude
normalized_magnitude = magnitude / magnitude.max()

# Calculate the luminance characters according to intensity
normalized_luminance = resized_image / 255

art = ""

edge_threshold = 0.8

for y in range(new_height):
    for x in range(new_width):
        if normalized_magnitude[y, x] > edge_threshold:
            ang = angle[y, x]
            for (low, high), char in edge_chars.items():
                if low <= ang < high:
                    ascii_char = char
                    break
        else:
            lum = normalized_luminance[y, x]
            lum_idx = int(lum * (len(luminance_char) - 1))
            ascii_char = luminance_char[lum_idx]

        art += ascii_char
    art += "\n"

# Definition as Stated in WCAG 2.
# Note 1: For the sRGB colorspace, the relative luminance of a color is defined as L = 0.2126 * R + 0.7152 * G + 0.0722 * B

def display_ascii_art(ascii_art:str):
    # Create the root window
    root = tk.Tk()
    root.title("ASCII Art")

    # Create a scrolled text widget to handle large content
    text_widget = tk.Label(root, text=ascii_art, font=("Courier", -8), justify=tk.LEFT)
    text_widget.pack(side="top", fill=tk.BOTH, expand=True)


    # Start the Tkinter event loop
    root.mainloop()

# Example usage
# Assuming 'ascii_art' contains the generated ASCII art as a single string
display_ascii_art(art)


"""
for y in range(resized.shape[0]):
    for x in range(resized.shape[1]):
        r, g, b = resized[y][x]
        
        r: int
        g: int
        b: int

        luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b)
        index = int(luminance / 255 * (len(ASCII_CHARS)-1))
        logging.info(f"This pixel: {resized[y][x]} has the following relative luminance: {luminance} which would have an index of: {index} matching this ASCII char: {ASCII_CHARS[index]}")
        art += ASCII_CHARS[index]
    art += "\n"

print(art)
# GUI
root = tk.Tk()
root.title("ASCII Video Player")
# im = Image.fromarray(cv2.threshold(dof, 200, 255, cv2.THRESH_BINARY)[1])
im = Image.fromarray(grad)
imgtk = ImageTk.PhotoImage(image=im)
tk.Label(root, image=imgtk).pack()
Label(
    root,
    justify=LEFT,
    text=text,
    font=("Courier", -8)
).pack()
root.mainloop()
"""
