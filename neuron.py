from random import random, randrange
from math import exp
from config import *


class Neuron:
    """ This is a neuron
    """
    def __init__(self, list_weight):
        """
        Inits a neuron that has list_weight as weights
        """
        self.list_weight = list_weight
        self.nbr_input = len(self.list_weight)

    @staticmethod
    def random_init(nbr_input):
        """
        Inits a neuron that takes 'nbr_input' inputs, and has random weights.
        :param nbr_input: the number of inputs of the neuron
        :return: a Neuron
        """
        return Neuron([Neuron.random_weight() for i in range(nbr_input)])

    @staticmethod
    def random_weight():
        """
        :return: a random weight between -1 and 1
        """
        return random()*2-1

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

    def mutation(self, avg):
        """
        Change randomly weights of this neuron
        """
        for i in range(len(self.list_weight)):
            if random() < avg:
                self.list_weight[i] = self.random_weight()
