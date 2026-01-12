from PIL import Image, ImageOps

class Texture:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.image = Image.open(filepath)

    def resize(self, cellSize: int):
        """
            Redimensionne l'image d'un objet à une taille carrée spécifiée.

            La méthode ajuste l'image contenue dans l'objet pour qu'elle ait
            une largeur et une hauteur égales à `cellSize`.

            Paramètres
            ----------
            cellSize : int
                Taille (en pixels) des côtés de l'image après redimensionnement.

            Retours
            -------
            self
                L'objet lui-même, permettant un chaînage de méthodes si nécessaire.
        """
        self.image = self.image.resize((cellSize, cellSize))
        return self

    def getGrayScale(self):
        """
            Convertit l'image de l'objet en niveaux de gris.

            La méthode transforme l'image en nuances de gris tout en conservant
            le canal alpha si l'image est en mode RGBA.
            - Pour les images RGBA : les canaux R, G et B sont convertis en gris
              et recombinés avec le canal alpha original.
            - Pour les autres images : l'image est convertie en niveaux de gris
              et recombinée sur les trois canaux RGB.

            Retours
            -------
            self
                L'objet lui-même avec l'image convertie en niveaux de gris.
        """
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
            Applique une colorisation à une image en niveaux de gris.

            La méthode prend une image en niveaux de gris (mode RGBA) et la
            transforme en image colorée en fonction des couleurs spécifiées
            pour les zones sombres et claires. L'opacité de la colorisation
            peut être ajustée.

            Paramètres
            ----------
            black_color : str, optionnel
                Couleur à appliquer aux parties les plus sombres de l'image.
                Par défaut "black".
            white_color : str, optionnel
                Couleur à appliquer aux parties les plus claires de l'image.
                Par défaut "white".
            color_opacity : float, optionnel
                Intensité de la colorisation, entre 0.0 et 1.0 :
                - 0.0 = aucune colorisation (image originale conservée)
                - 1.0 = colorisation complète
                Par défaut 1.0.

            Retours
            -------
            Image
                L'image colorisée résultante (mode RGBA).

            Exceptions
            ----------
            Exception
                Levée si l'image n'est pas en mode RGBA (doit être en niveaux de gris).
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
        """
            Retourne l'image associée à l'objet.

            Cette méthode permet d'accéder à l'image actuelle de l'objet,
            après tout traitement éventuel (redimensionnement, niveaux de gris,
            colorisation, etc.).

            Retours
            -------
            Image
                L'image actuelle de l'objet.
        """
        return self.image
