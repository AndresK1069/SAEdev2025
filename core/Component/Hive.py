from core.Player import Player


class Hive(object):
    def __init__(self, displayObject: str , owner: Player):
        self.displayObject = displayObject
        self.owner = owner
