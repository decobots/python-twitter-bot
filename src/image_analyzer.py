import io

from PIL import Image
from PIL import ImageStat

from src.color_table import Color


class ImageAnalazer:
    def __init__(self, data: bytes):
        self.image = Image.open(io.BytesIO(data))

    @property
    def avg_color(self) -> 'Color':
        r, g, b = ImageStat.Stat(self.image).mean
        return Color(r, g, b)
