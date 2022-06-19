import argparse

from pathlib import Path

import numpy as np

from numpy.typing import ArrayLike
from PIL import Image

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczmwqpdbkhao*XYUJCLQ0OZ#MW&8%B@$"
MAX_PIXEL_VALUE = 255


Pixel = list[int, int, int]
MyImage = ArrayLike[Pixel]
ASCIIChar = str
ASCIIImage = list[list[ASCIIChar]]


# TODO: Return list of list of tuples representing RGB values
def load_image(path: Path) -> MyImage:
    with Image.open(path) as image:
        return np.array(image.getdata())


# TODO: Implement the two functions below
def save_image(image: MyImage, path: Path) -> None:
    pass


def default_save(path: Path) -> Path:
    pass


def brightness(pixel: Pixel) -> float:
    n = len(pixel)
    avg = sum(pixel) / n
    return min(avg, MAX_PIXEL_VALUE)


def nearest_ascii_char(pixel_brightness: float) -> ASCIIChar:
    n = len(ASCII_CHARS)
    output, diff = ASCII_CHARS[0], pixel_brightness
    for i in range(n):
        curr_diff = abs(pixel_brightness - (i * MAX_PIXEL_VALUE / (n - 1)))
        if curr_diff < diff:
            output = ASCII_CHARS[i]
            diff = curr_diff

    return output


# TODO: Fix Mapping
def asciify(image: MyImage) -> ASCIIImage:
    return list(map(nearest_ascii_char, map(brightness, image)))


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert image to ASCII image')
    parser.add_argument('image', help='The path to the image you want to convert')
    parser.add_argument('-o', default=None, help="output file name")

    args = parser.parse_args()
    file_path = Path(args.image)
    if not file_path.exists():
        print(f"File {file_path.name} does not exist")
        return

    print(f"Loading file {file_path.name}")
    image = load_image(file_path)
    print("Converting file")
    output = asciify(image)

    output_name = file_path.name
    print(f"Finished! File saved as {output_name}")
    save_image(output, output_name)
    print(output)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
