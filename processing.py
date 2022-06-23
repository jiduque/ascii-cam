import warnings

from functools import partial

from data import *

warnings.filterwarnings("ignore", category=DeprecationWarning)


def preprocess_image(image: Image) -> Image:
    basewidth = 300
    width, height = image.size
    wpercent = (basewidth / float(width))
    hsize = int((float(height) * float(wpercent)))
    return image.resize((basewidth, hsize), Image.ANTIALIAS)


def to_array(image: Image) -> ImageArray:
    width, height = image.size
    pixels = list(image.getdata())
    return [pixels[i:i + width] for i in range(0, len(pixels), width)]


def brightness(pixel: Pixel) -> float:
    # luminosity weights
    weights = (0.21, 0.72, 0.07)

    output = 0
    for p, w in zip(pixel, weights):
        output += p * w

    return min(output, MAX_PIXEL_VALUE)


def brightness_matrix(image: ImageArray) -> BrightnessArray:
    return [list(map(brightness, row)) for row in image]


def normalize_brightness(brightness_mat: BrightnessArray) -> BrightnessArray:
    max_pixel = max(max(x) for x in brightness_mat)
    min_pixel = min(min(x) for x in brightness_mat)

    output = brightness_mat.copy()

    for i, row in enumerate(brightness_mat):
        for j, pixel in enumerate(row):
            output[i][j] = MAX_PIXEL_VALUE * (pixel - min_pixel) / float(max_pixel - min_pixel)

    return output


def ascii_char(pixel_brightness: float, ascii_map: ASCIIMap = ASCIIMap) -> ASCIIChar:
    n = len(ascii_map)
    i_hat = (n - 1) * pixel_brightness / MAX_PIXEL_VALUE
    index = round(i_hat)
    return ascii_map[index]


def asciify(brightness_mat: BrightnessArray, ascii_map: ASCIIMap = ASCII_CHARS) -> ASCIIImage:
    map_func = partial(ascii_char, ascii_map=ascii_map)
    return [list(map(map_func, row)) for row in brightness_mat]


def convert(ascii_map: ASCIIMap, image: ImageArray) -> ASCIIImage:
    brightness_mat = brightness_matrix(image)
    normalized_mat = normalize_brightness(brightness_mat)
    return asciify(normalized_mat, ascii_map)
