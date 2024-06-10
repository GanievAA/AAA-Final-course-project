from io import BufferedReader, BytesIO
from base64 import b64encode
from typing import List, Tuple

from PIL import Image, ImageFont
from PIL.ImageDraw import Draw


Coords = List[List[int]]  # EasyOCR format
Box = Tuple[int, int, int, int]  # PIL format


def open_image(image_fp: BufferedReader) -> Image:
    return Image.open(image_fp)


class PolygonDrawer:
    def __init__(self, image: Image) -> None:
        self._clean_image = image.copy()
        self._image = image
        self._draw = Draw(image)

    @staticmethod
    def coords_to_box(coords: Coords) -> Box:
        """Convert EasyOCR coords to PIL box format"""
        return coords[0], coords[1], coords[2], coords[3]

    def highlight_word(self, coords: Coords, word: str) -> None:
        """Add polygon at given coords and add word"""
        box = self.coords_to_box(coords)
        self._draw.rectangle(box, outline="green", width=2)
        text_height = 12  # px, hardcoded
        x, y = box[:2]
        self._draw.text((x, y - text_height), word, font=ImageFont.load_default(size=11), fill="green")

    def crop(self, coords: Coords) -> Image:
        """Get cropped Image part"""
        box = self.coords_to_box(coords)
        return self._clean_image.crop(box)

    def get_highlighted_image(self) -> Image:
        """Get result Image with highlights"""
        return self._image


def image_b64encode(image: Image) -> str:
    with BytesIO() as io:
        image.save(io, format="png", quality=100)
        io.seek(0)
        return b64encode(io.read()).decode()


def image_to_img_src(image: Image) -> str:
    return f"data:image/png;base64,{image_b64encode(image)}"
