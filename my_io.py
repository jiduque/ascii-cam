from processing import convert, preprocess_image, to_array
from data import Image, ImageArray, ASCIIMap, ASCIIImage, Frame, Path


def load_image(path: Path) -> ImageArray:
    with Image.open(path) as image:
        new_image = preprocess_image(image)
        output = to_array(new_image)
        return output


def save_image(image: ASCIIImage, path: Path) -> None:
    with path.open(mode='w') as file:
        output_string = '\n'.join([''.join(row) for row in image])
        file.write(output_string)


# TODO: Make this function better
def render(ascii_map: ASCIIMap, frame: Frame) -> None:
    image = Image.fromarray(frame)
    new_image = to_array(preprocess_image(image))
    ascii_image = convert(ascii_map, new_image)
    print("Here is frame:")
    print(ascii_image)
