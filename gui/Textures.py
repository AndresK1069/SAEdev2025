from PIL import Image, ImageOps

class Texture:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.image = Image.open(filepath)

    def resize(self, cellSize: int):
        self.image = self.image.resize((cellSize, cellSize))
        return self

    def getGrayScale(self):
        if self.image.mode == "RGBA":
            r, g, b, a = self.image.split()
            gray = Image.merge("RGB", (r, g, b)).convert("L")
            self.image = Image.merge("RGBA", (gray, gray, gray, a))
        else:
            gray = self.image.convert("L")
            self.image = Image.merge("RGB", (gray, gray, gray))
        return self

    def getColorize(self, black_color="black", white_color="white", color_opacity=1.0):
        """
        color_opacity: float between 0.0 and 1.0
            0.0 = no colorization
            1.0 = full colorization
        """
        if self.image.mode != "RGBA":
            raise Exception("Image must be a grayscale image")
        original = self.image
        r, g, b, a = original.split()
        gray = Image.merge("RGB", (r, g, b)).convert("L")
        colored = ImageOps.colorize(
            gray,
            black=black_color,
            white=white_color
        ).convert("RGBA")
        colored.putalpha(a)
        self.image = Image.blend(original, colored, color_opacity)
        return self.image

    def getImage(self):
        return self.image
