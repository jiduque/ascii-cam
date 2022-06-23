import curses
import time

from curses import window

from processing import convert, preprocess_image, to_array
from data import Image, ImageArray, ASCIIMap, ASCIIImage, Frame, Path


UPDATE_RATE = 0.15


def load_image(path: Path, size: tuple[int, int] | None = None) -> ImageArray:
    with Image.open(path) as image:
        new_image = preprocess_image(image, size)
        output = to_array(new_image)
        return output


def save_image(image: ASCIIImage, path: Path) -> None:
    with path.open(mode='w') as file:
        output_string = '\n'.join([''.join(row) for row in image])
        file.write(output_string)


def show(ascii_image: ASCIIImage, stdscr: window) -> None:
    n, m = len(ascii_image), len(ascii_image[0])
    stdscr.clear()
    for i in range(n):
        for j in range(m):
            t = ascii_image[i][j]
            stdscr.addstr(i, j, t)
    stdscr.refresh()

    time.sleep(UPDATE_RATE)


def render(ascii_map: ASCIIMap, frame: Frame, stdscr: window) -> None:
    window_size = stdscr.getmaxyx()
    size = (window_size[0] - 5, window_size[1] - 5)

    image = Image.fromarray(frame)
    new_image = to_array(preprocess_image(image, size))
    ascii_image = convert(ascii_map, new_image)
    show(ascii_image, stdscr)
