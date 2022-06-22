import argparse

from pathlib import Path

from data import *
from processing import convert

from PIL import Image


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
