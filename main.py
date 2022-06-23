import curses

import processing

from data import ASCII_CHARS, Path
from my_io import render, load_image, save_image

import click
import cv2


def default_output_name(path: Path) -> Path:
    name_split = path.name.split('.')
    name = ''.join(name_split[:-1])
    return Path(f"{name}_ascii.txt")


@click.group("askey")
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
    ascii_map = ASCII_CHARS
    if invert:
        ascii_map = list(reversed(ascii_map))

    vc = cv2.VideoCapture(0)
    rval = False
    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()

    stdscr = curses.initscr()
    while rval:
        rval, frame = vc.read()
        render(ascii_map, frame, stdscr)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    stdscr.clear()


if __name__ == '__main__':
    cli.add_command(convert, 'convert')
    cli.add_command(stream, 'stream')
    cli()
