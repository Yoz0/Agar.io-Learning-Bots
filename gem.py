from random import random, randrange

from config import *

class Gem:
    """
    This is a gem
    """
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.marge = 2
        self.sprite = canvas.create_rectangle(self.i * SQUARE_SIZE + self.marge, self.j * SQUARE_SIZE + self.marge,
                                         (self.i + 1) * SQUARE_SIZE - self.marge, (self.j+1) * SQUARE_SIZE - self.marge,
                                         fill=Gem.random_color())

    def erase(self):
        """
        Erase the sprite from the canvas
        """
        canvas.delete(self.sprite)

    @staticmethod
    def random_color():
        red = randrange(255)
        blue = randrange(255)
        green = randrange(255)
        res = "#"
        for i in [red, green, blue]:
            if i < 16:
                res += "0"+hex(i)[-1:].upper()
            else:
                res += hex(i)[-2:].upper()
        return res

    @staticmethod
    def detect_gem(i, j, list_gem):
        """
        Detect if there is a foe at the location i,j
        :param i: the line
        :param j: the column
        :return: the gem if there is one, None if there isn't
        """
        k = 0
        while k < len(list_gem):
            gem = list_gem[k]
            if gem.i == i and gem.j == j:
                return gem
            k += 1
        return None
