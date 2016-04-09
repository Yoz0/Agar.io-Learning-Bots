from math import sqrt
from gem import *
from neuron import *
from layer import *
from neuralnetwork import *
from useful import *
from config import *
from bot import *


class BotV2(Bot):
    """
    This is a bot.
    """

    def __init__(self, canvas, brain, i, j, name="unnamed"):
        """
        inits a bot whose brain is made of a neural network.
        """

        if not isinstance(brain, NeuralNetwork):
            raise TypeError("in 'BotV2.__init()': you have not given a neural network as brain.")

        self.nbr_inputs = (NBR_BOT + NBR_GEMS - 1) * 3
        if brain.nbr_input != self.nbr_inputs:
            raise ValueError("in 'BotV2.__init()': the brain you provided do not have the right number of input.")

        super(BotV2, self).__init__(canvas, brain, name)
        self.i = i
        self.j = j

        self.list_input = [0 for i in range(self.nbr_inputs)]
        self.list_output = [0, 0, 0, 0]  # up / down / left / right

    @staticmethod
    def quick_init(canvas, i=0, j=0, name="unnamed"):
        """
        Returns a bot whose brain was inited with random weights
        """
        # the 'list_sizes' and 'nbr_inputs' args of 'NeuralNetwork.quick_init()' are
        # hardcoded because botv1 should always have a brain with this structure.
        return BotV2(canvas,
                     NeuralNetwork.quick_init([NBR_BOT+NBR_GEMS, 4], (NBR_BOT + NBR_GEMS - 1) * 3),
                     i, j,
                     name)

    def mate_with(self, bot2, name="unnamed"):
        """
        Creates a new bot (bot3), crossover from bot1 and bot2. The new bot takes exactly
        (and for each layer) half his neurons from 'bot1' and the other half from 'bot2' :
        only the distribution on each layer is random.
        :param name: name of the newly created bot
        :param bot2: other bot to mate with
        :return: a new bot with, on each layer of his neural network, as many
                 neurons from bot 1 as bot 2.
        """
        bot3 = BotV2(self.canvas, self.brain.crossover(bot2.brain), randrange(WIDTH), randrange(HEIGHT), name)
        return bot3

    def mutation(self, avg):
        """
        Mutate (or not) the bot
        :param avg: the avergae of bot who will be mutated if you call this function with a tons of bot
        :return:
        """
        self.brain.mutation(avg)

    def update_input(self, list_bot, list_gem):
        """
        watches everything the board and updates list_input accordingly
        """
        self.list_input.clear()

        for gem in list_gem:
            self.list_input.append(gem.i-self.i)
            self.list_input.append(gem.j-self.j)
            distance = sqrt((gem.i-self.i)**2 + (gem.j-self.j)**2)
            self.list_input.append(int(distance))

        for bot in list_bot:
            if bot != self:
                self.list_input.append(bot.i-self.i)
                self.list_input.append(bot.j-self.j)
                distance = sqrt((gem.i-self.i)**2 + (gem.j-self.j)**2)
                if(bot.strength > self.strength):
                    self.list_input.append(int(-distance))
                else:
                    self.list_input.append(int(distance))

        if len(self.list_input) > self.nbr_inputs:
            raise ValueError("In 'BotV2.update_input()' : too much objects. len(list_input) = " + str(len(self.list_input)))

        while len(self.list_input) < self.nbr_inputs:
            self.list_input.append(0)

    def move(self):
        """
        Checks which output is the "most activated" (which is higher) and move
        in that direction.
        :return:
        """

        # #check if every output is the same
        # all_same = 1        #let's assert all output is the same
        # first_value = self.list_output[0]
        # for value in self.list_output:
        #     if value != first_value:
        #         all_same = 0
        #         break

        # if all_same:
        #     i_max = randrange(4)
        # else:
        i_max = max_index(self.list_output)

        if i_max == 0 and self.j > 0:
            self.j -= 1
        elif i_max == 1 and self.j < HEIGHT-1:
            self.j += 1
        elif i_max == 2 and self.i > 0:
            self.i -= 1
        elif i_max == 3 and self.i < WIDTH-1:
            self.i += 1
