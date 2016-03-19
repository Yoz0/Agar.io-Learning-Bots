"""
file: utility.py
This file holds usefull functions that can be reused in other programms
"""

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