from data.constante import MAX_NECTAR

class Flower:
    def __init__(self,displayObject: str , flowerNectar : int):
        self.displayObject = displayObject
        self.flowerNectar = flowerNectar

    def reduceNectar(self) -> int:
        ratio = self.flowerNectar / MAX_NECTAR
        if ratio >= 2 / 3:
            self.flowerNectar -=3
            return 3
        elif ratio > 1 / 3:
            self.flowerNectar -= 2
            return 2
        else:
            self.flowerNectar -= 1
            return 1