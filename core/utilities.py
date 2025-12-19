from core.Component.Bees.BeeTypes import BEE_TYPES


def evenSplit(nfleur: int , maxNectar :int) -> int:
    return maxNectar//(nfleur*2)

def getBeeStats(string:str):
    string.lower()
    bee_class = BEE_TYPES[string]
    return bee_class()