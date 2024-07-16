import logging
import cv2 as cv
import numpy as np
from numpy.typing import NDArray

EDGE_THRESHOLD = 0.9
THRESHOLD_VALUE = 1.75

EDGE_CHARS = {
    (337.5, 360): "-",
    (0, 22.5): "-",  # Horizontal line at near 0 or 360 degrees
    (22.5, 67.5): "/",  # 45 degrees (positive diagonal)
    (67.5, 112.5): "|",  # Vertical line
    (112.5, 157.5): "\\",  # 135 degrees (negative diagonal)
    (157.5, 202.5): "-",  # Horizontal line
    (202.5, 247.5): "/",  # Negative diagonal
    (247.5, 292.5): "|",  # Vertical line
    (292.5, 337.5): "\\",  # Positive diagonal
}

LUMINANCE_CHARS = "\u00a0.,:;iIPEOB#■■"


def frame_2_ascii(frame: NDArray[...]) -> str:
    logger = logging.getLogger(__name__)
    logging.debug(f"Frame:\n{frame}")
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    WIDTH = 180
    HEIGHT = 101

    aspect_ratio = gray_frame.shape[1] / gray_frame.shape[0]
    new_width = WIDTH
    new_height = int(WIDTH / (2 * aspect_ratio))
    if new_height > HEIGHT:
        new_height = HEIGHT
        new_width = int(HEIGHT * aspect_ratio * 2)

    resized_frame = cv.resize(
        gray_frame, (new_width, new_height), interpolation=cv.INTER_AREA
    )

    if logging.getLevelName(logger.getEffectiveLevel()) == "DEBUG":
        cv.imshow("resized_frame", resized_frame)
        _ = cv.waitKey(0)
    blur1 = cv.GaussianBlur(resized_frame, (5, 5), 0)
    blur2 = cv.GaussianBlur(resized_frame, (9, 9), 0)

    dog = cv.subtract(blur1, blur2)

    _, thresholded_dog = cv.threshold(dog, THRESHOLD_VALUE, 255, cv.THRESH_BINARY)

    grad_x = cv.Scharr(thresholded_dog, cv.CV_32F, 1, 0)
    grad_y = cv.Scharr(thresholded_dog, cv.CV_32F, 0, 1)

    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    angle = np.arctan2(grad_y, grad_x) * (180 / np.pi)

    angle = np.mod(angle + 360, 360)

    if magnitude.max() == 0:
        normalized_magnitude = np.zeros_like(magnitude)
    else:
        normalized_magnitude = magnitude / magnitude.max()

    normalized_luminance = resized_frame / 255

    final_string = ""

    for y in range(new_height):
        for x in range(new_width):
            ascii_char = ""
            if normalized_magnitude[y, x] > EDGE_THRESHOLD:
                ang = angle[y, x]
                for (low, high), char in EDGE_CHARS.items():
                    if low <= ang <= high:
                        ascii_char = char
                        break
            else:
                lum = normalized_luminance[y, x]
                lum_idx = int(lum * (len(LUMINANCE_CHARS) - 1))
                ascii_char = LUMINANCE_CHARS[lum_idx]

            final_string += ascii_char
        final_string += "\n"

    return final_string
