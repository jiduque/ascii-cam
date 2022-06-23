from pathlib import Path

from numpy.typing import ArrayLike
from PIL import Image

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255


Image = Image
Path = Path


ASCIIMap = str

Pixel = list[int, int, int]
ImageArray = list[list[Pixel]]

Brightness = float
BrightnessArray = list[list[Brightness]]

ASCIIChar = str
ASCIIImage = list[list[ASCIIChar]]

Frame = ArrayLike
