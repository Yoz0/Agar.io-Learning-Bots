from random import random, randrange
from math import exp
from config import *


class Neuron:
    """ This is a neuron
    """
    def __init__(self, arg1):
        """
        method 1 : my_neuron = Neuron(nbr_input)
            Inits a neuron that takes 'nbr_input' inputs, and has random weights.
        method 2 : my_neuron = Neuron(list_weight)
            Inits a neuron that has list_weight as weights, and as many inputs
        """
        if isinstance(arg1, int):
            #method 1
            self.nbr_input = arg1
            self.list_weight = Neuron.list_weight_random(self.nbr_input)
        elif isinstance(arg1, list):
            #method 2
            self.list_weight = arg1
            self.nbr_input = len(self.list_weight)

    def __str__(self):
        return "id : " + str(id(self)) + " list of weight" + str(self.list_weight)

    def output(self, list_input):
        """
        :param list_input: a list of input (numbers). The length of this list should be the nbr_input entered at the creation
        :return: a positive number calculated from the input
        """
        if len(list_input) != len(self.list_weight):
            raise ValueError("In Neuron.output() the input you provided has not the good size")
        res = 0
        for i in range(self.nbr_input):
            res += self.list_weight[i] * list_input[i]
        return 1 / (1 + exp(-res))

    def mutation(self):
        """
        Change randomly one weight on the list_weight
        """
        i = randrange(self.nbr_input)
        self.list_weight[i] = Neuron.random_weight()

    @staticmethod
    def random_weight():
        """
        :return: a random weight between -1 and 1
        """
        return random()*2-1

    @staticmethod
    def list_weight_random(nbr_input):
        """
        :param nbr_input: the size of the desired list
        :return: a list of random weight.
        """
        res = []
        for i in range(nbr_input):
            res.append(Neuron.random_weight())
        return res
