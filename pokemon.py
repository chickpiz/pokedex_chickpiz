# pokemon.py
from basic import Basic
from battle import Battle
from breed import Breed


class Pokemon:

    def __init__(self):
        self.Basic = Basic()
        self.Battle = Battle()
        self.Breed = Breed()
