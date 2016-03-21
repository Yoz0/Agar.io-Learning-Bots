from gem import *
from neuron import *
from layer import *
from neural_network import *
from useful import *
from config import *


class Bot:
    """
    This is a bot.
    """

    def __init__(self, nbr_input, brain, i, j, name = "unnamed"):
        """
        inits a bot whose brain is made of a neural network. The neural network
        structure is given by 'list_sizes' where 'list_sizes[n]' is the size of the
        nth layer of the network, and 'nbr_input' is the number of input that each
        neuron of the first layer take.
        """

        self.name = name
        self.brain = brain
        self.i = i
        self.j = j
        self.strength = 0
        self.list_input = [0 for i in range(nbr_input)]
        self.list_output = [0, 0, 0, 0]  # up / down / left / right
        self.sprite = None

    def get_name(self):
        return self.name

    def get_full_id(self):
        res = "id: " + str(id(self))
        res += " position: i = " + str(self.i) + " ; j = " + str(self.j)
        res += "Strength: " + str(self.strength)
        res += "\n Neurons:\n"
        for i, layer in ennumerate(brain):
            for neuron in layer:
                res += "Layer " + i + " - "
                res += str(neuron)
            res += "\n"

        return res

    def __str__(self):
        return self.get_name() + " Strength: " + str(self.strength)

    def reset(self):
        """keeps the brain as it is, but resets the strengh and the position"""
        self.i = randrange(WIDTH)
        self.j = randrange(HEIGHT)
        self.strength = 0

    def display(self):
        """
        Display the bot at the position i;j on the canvas.
        Canvas should be a global ariable.
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

    def update(self, list_bot, list_gem):
        """
        Compute the input
        Calculate the output
        Move according to the output
        and update the display
        """
        self.update_input(list_bot, list_gem)
        self.update_output()
        self.move()
        self.display()

    def update_input(self, list_bot, list_gem):
        """
        Check up, down, left and right to see if there is any foe or gem and update self.list_input accordingly
        """
        self.list_input = [0 for k in range(8)]
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

    def detect_foe(self, i, j, list_bot):
        """
        Detect if there is a foe (a bot different than me) at the location i, j
        :param i: the line
        :param j: the column
        :return: the foe if there is one, None if not.
        """
        k = 0
        while k < len(list_bot):
            foe = list_bot[k]
            if foe.i == i and foe.j == j and self != foe:
                return foe
            k += 1
        return None

    def update_output(self):
        """
        Feeds the brain (neural_network) with 'list_input', and updates 'list_output'
        accordingly.
        """
        self.list_output = self.brain.get_output(self.list_input)

    def move(self):
        """
        Check which out put is the "most activated" (which is higher) and move in that direction
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

    def eat(self, list_bot, list_gem, list_dead_bot):
        """
        Check if there is a weaker foe or a Gem at my location, if so, eat it!
        """
        gem = Gem.detect_gem(self.i, self.j, list_gem)
        if gem is not None:
            if self.strength < MAX_STRENGTH:
                self.strength += 1
            gem.erase()
            list_gem.remove(gem)

        foe = self.detect_foe(self.i, self.j, list_bot)
        if foe is not None:
            if(foe.strength <= self.strength):
                for i in range(5):
                    if self.strength+1 <= MAX_STRENGTH:
                        self.strength += 1
                foe.erase()
                list_dead_bot.append(foe)
                list_bot.remove(foe)