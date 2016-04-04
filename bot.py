from abc import ABCMeta, abstractmethod
from useful import *
from copy import *
from layer import *
from neuralnetwork import *


class Bot(metaclass=ABCMeta):
    """
    Abstract class.
    This is a bot.
    """

    @abstractmethod
    def __init__(self, canvas, brain, name="unnamed"):
        """
        inits a bot whose brain is made of a neural network.
        """

        self.name = name
        self.brain = brain
        self.strength = 0
        self.i = None
        self.j = None
        self.sprite = None
        self.list_input = None      # list of inputs gathered every turn with update_input()
        self.list_output = None     # list of outputs computed every turn with update_output()

    def __str__(self):
        return self.name + " Strength: " + str(self.strength)

    def get_full_id(self):
        res = "id: " + str(id(self))
        res += " position: i = " + str(self.i) + " ; j = " + str(self.j)
        res += "Strength: " + str(self.strength)
        res += "\n Neurons:\n"
        for i, layer in enumerate(self.brain):
            for neuron in layer:
                res += "Layer " + i + " - "
                res += str(neuron)
            res += "\n"
        return res

    def reset(self):
        """keeps the brain as it is, but resets the strength and the position"""
        self.i = randrange(WIDTH)
        self.j = randrange(HEIGHT)
        self.strength = 0

    def display(self):
        """
        Display the bot at the position i;j on the canvas.
        Canvas should be a global variable.
        """
        self.canvas.delete(self.sprite)
        self.sprite = self.canvas.create_oval(self.i * SQUARE_SIZE, self.j * SQUARE_SIZE,
                                         (self.i + 1) * SQUARE_SIZE, (self.j+1) * SQUARE_SIZE,
                                         fill=int_to_color(self.strength, MAX_STRENGTH))

    def erase(self):
        """
        Erase the sprite from canvas
        """
        self.canvas.delete(self.sprite)

    @abstractmethod
    def update(self, list_bot, list_gem):
        """
        Compute the input
        Calculate the output
        Move according to the output
        and update the display
        """
        pass

    @abstractmethod
    def update_input(self, list_bot, list_gem):
        """
        Updates the bot's 'list_input' from what he can see of his environement
        """
        pass

    def update_output(self):
        """
        Feeds the brain (neural_network) with 'list_input', and updates 'list_output'
        accordingly.
        """
        self.list_output = self.brain.get_output(self.list_input)

    @abstractmethod
    def move(self):
        """Checks which output is the "most activated" (which is higher), and
        moves accordingly"""
        pass

    def inc_strength(self, incr):
        """
        increment the strength of the bot
        :param incr: how much we should increment the strength
        """
        if self.strength + incr < MAX_STRENGTH:
            self.strength += incr
        else:
            self.strength = MAX_STRENGTH


def bot_sort(list_of_bots):
    """
    Sorts 'list_of_bots' with strength decreasing.
    :param list_of_bots: list of bots to sort
    """
    for i in range(len(list_of_bots)-1):
        if list_of_bots[i].strength < list_of_bots[i+1].strength:
            list_of_bots[i], list_of_bots[i + 1] = list_of_bots[i + 1], list_of_bots[i]
            temp = i
            while temp > 0 and list_of_bots[temp].strength > list_of_bots[temp-1].strength:
                list_of_bots[temp], list_of_bots[temp - 1] = list_of_bots[temp - 1], list_of_bots[temp]
                temp -= 1
