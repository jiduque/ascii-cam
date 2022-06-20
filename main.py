import warnings
import argparse

from pathlib import Path
from functools import partial

from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255


Pixel = list[int, int, int]
ImageArray = list[list[Pixel]]
Brightness = float
BrightnessArray = list[list[Brightness]]
ASCIIMap = str
ASCIIChar = str
ASCIIImage = list[list[ASCIIChar]]


def preprocess_image(image: Image) -> Image:
    basewidth = 300
    width, height = image.size
    wpercent = (basewidth / float(width))
    hsize = int((float(height) * float(wpercent)))
    return image.resize((basewidth, hsize), Image.ANTIALIAS)


def load_image(path: Path) -> ImageArray:
    with Image.open(path) as image:
        new_image = preprocess_image(image)
        width, height = new_image.size
        pixels = list(new_image.getdata())
        return [pixels[i:i + width] for i in range(0, len(pixels), width)]


def save_image(image: ASCIIImage, path: Path) -> None:
    with path.open(mode='w') as file:
        output_string = '\n'.join([''.join(row) for row in image])
        file.write(output_string)


def default_output_name(path: Path) -> Path:
    name_split = path.name.split('.')
    name = ''.join(name_split[:-1])
    return Path(f"{name}_ascii.txt")


def brightness(pixel: Pixel) -> float:
    # luminosity weights, avg is 1/3, 1/3, 1/3
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


class CLI:
    def __init__(self):
        self.ascii_map = ASCII_CHARS

    def __call__(self) -> None:
        self.main()

    def parse_args(self) -> tuple[Path, Path]:
        parser = argparse.ArgumentParser(description='Convert image to ASCII image')
        parser.add_argument('image', help='The path to the image you want to convert')
        parser.add_argument('-o', default=None, help="output file name")
        parser.add_argument('--invert', action=argparse.BooleanOptionalAction)

        args = parser.parse_args()

        file_path = Path(args.image)
        output_name = default_output_name(file_path)

        if args.o and not Path(args.o).exists():
            output_name = Path(args.o)

        if args.invert:
            self.ascii_map = ''.join(reversed(self.ascii_map))

        return file_path, output_name

    def main(self) -> None:
        file_path, output_name = self.parse_args()

        if not file_path.exists():
            print(f"File {file_path.name} does not exist")
            return

        print(f"Loading file {file_path.name}")
        image = load_image(file_path)

        print("Converting file")
        output = convert(self.ascii_map, image)
        print(f"Finished!")

        save_image(output, output_name)
        print(f"File saved as {output_name.name}")


if __name__ == '__main__':
    main = CLI()
    main()
