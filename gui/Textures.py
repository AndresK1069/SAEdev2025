from PIL import Image, ImageOps

class Texture:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def resize(self, cellSize: int):
        image = Image.open(self.filepath)
        return image.resize((cellSize, cellSize))

    def getGrayScale(self, image: Image.Image):
        return image.convert('L')

    def colorize(self, image: Image.Image, black_color: str = "black", white_color: str = "white"):
        if image.mode != 'L':
            image = image.convert('L')
        return ImageOps.colorize(image, black=black_color, white=white_color)
