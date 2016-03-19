"""
file: utility.py
This file holds usefull functions that can be reused in other programms
"""

from random import randrange
from config import *

def max_index(list_int):
    """
    :param list_int: a list of numbers
    :return: the index of the maximum
    """
    i_max = 0
    maxi = - float('inf')
    for i in range(len(list_int)):
        if list_int[i] > maxi:
            i_max = i
            maxi = list_int[i]
    return i_max

def int_to_color(strength):
    """
    :param strength: a number between 0 and 'MAX_STRENGTH'
    :return: a string like "#RRGGBB" which can be interpreted as a color
    (the higher the strength is, the reder the color is)
    """

    red = strength * 255 // MAX_STRENGTH
    blue = 255 - red
    green = 0
    res = "#"
    for i in [red, green, blue]:
        if i < 16:
            res += "0"+hex(i)[-1:].upper()
        else:
            res += hex(i)[-2:].upper()
    return res

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