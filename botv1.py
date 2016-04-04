from gem import *
from neuron import *
from layer import *
from neuralnetwork import *
from useful import *
from config import *
from bot import *


class BotV1(Bot):
    """
    This is a bot.
    """

    def __init__(self, canvas, brain, i, j, name="unnamed"):
        """
        inits a bot whose brain is made of a neural network.
        """

        if not isinstance(brain, NeuralNetwork):
            raise TypeError("in 'BotV1.__init()': you have not given a neural network as brain.")

        super(BotV1, self).__init__(canvas, brain, name)
        self.i = i
        self.j = j
        self.list_input = [0 for i in range(8)] #this is hardcoded because we're in bot_v1
        self.list_output = [0, 0, 0, 0]  # up / down / left / right

    @staticmethod
    def quick_init(canvas, i=0, j=0, name="unnamed"):
        """
        Returns a bot whose brain was inited with random weights
        """
        # the 'list_sizes' and 'nbr_inputs' args of 'NeuralNetwork.quick_init()' are
        # hardcoded because botv1 should always have a brain with this structure.
        return BotV1(canvas,
                     NeuralNetwork.quick_init([4], 8),
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

        bot3 = BotV1(self.canvas, self.brain.crossover(bot2.brain), randrange(WIDTH), randrange(HEIGHT), name)

        return bot3

    def update_input(self, list_bot, list_gem):
        """
        Check up, down, left and right to see if there is any foe or gem and update self.list_input accordingly
        """
        self.list_input = [0 for k in range(self.brain.nbr_input)]

        if Gem.detect_gem(self.i, self.j - 1, list_gem) is not None:
            self.list_input[0] = 1
        if Gem.detect_gem(self.i, self.j + 1, list_gem) is not None:
            self.list_input[1] = 1
        if Gem.detect_gem(self.i - 1, self.j, list_gem) is not None:
            self.list_input[2] = 1
        if Gem.detect_gem(self.i + 1, self.j, list_gem) is not None:
            self.list_input[3] = 1

        foe = self.detect_foe(self.i, self.j - 1, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[4] = 1
            else:
                self.list_input[4] = -1
        foe = self.detect_foe(self.i, self.j + 1, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[5] = 1
            else:
                self.list_input[5] = -1
        foe = self.detect_foe(self.i - 1, self.j, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[6] = 1
            else:
                self.list_input[6] = -1
        foe = self.detect_foe(self.i + 1, self.j, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[7] = 1
            else:
                self.list_input[7] = -1

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
