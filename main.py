import argparse

from pathlib import Path

import processing
from data import ImageArray, ASCIIImage, ASCII_CHARS

import click

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


@click.group("ask_y")
def cli() -> None:
    pass


@click.command()
@click.argument('image')
@click.option('-i', '--invert', 'invert', is_flag=True)
@click.option('-o', '--output', 'output')
def convert(image: str, invert: bool = False, output: str | None = None) -> None:
    file_path = Path(image)
    if not file_path.exists():
        print(f"File {file_path.name} does not exist")
        return

    output_name = default_output_name(file_path)
    if output and not Path(output).exists():
        output_name = Path(output)

    ascii_map = ASCII_CHARS
    if invert:
        ascii_map = list(reversed(ascii_map))

    print(f"Loading file {file_path.name}")
    image = load_image(file_path)

    print("Converting file")
    ascii_pic = processing.convert(ascii_map, image)
    print(f"Finished!")

    save_image(ascii_pic, output_name)
    print(f"File saved as {output_name.name}")


@click.command()
@click.option('-i', '--invert', 'invert', is_flag=True)
def stream(invert: bool = False) -> None:
    print(f"Not working yet, bud. But {invert=}.")


if __name__ == '__main__':
    cli.add_command(convert, 'convert')
    cli.add_command(stream, 'stream')
    cli()

# TODO: Use this shit to get webcam streaming
# TODO: make io modules that will have the load/save image funcs and the CV webcam stuff
'''
import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
'''