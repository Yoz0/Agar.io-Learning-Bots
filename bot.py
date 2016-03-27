from abc import ABCMeta, abstractmethod
from config import *
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
    def __init__(self, brain, name="unnamed"):
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

    @staticmethod
    def quick_init(name="unnamed"):
        return Bot(NeuralNetwork.quick_init(), name)

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
        canvas.delete(self.sprite)
        self.sprite = canvas.create_oval(self.i * SQUARE_SIZE, self.j * SQUARE_SIZE,
                                         (self.i + 1) * SQUARE_SIZE, (self.j+1) * SQUARE_SIZE,
                                         fill=int_to_color(self.strength))

    def erase(self):
        """
        Erase the sprite from canvas
        """
        canvas.delete(self.sprite)

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

