from math import exp
from random import random, randrange
import tkinter as tk


class Neuron:
    """ This is a neuron
    """
    def __init__(self, nbr_input):
        self.list_weight = Neuron.list_weight_random(nbr_input)

    def __str__(self):
        return "id : " + str(id(self)) + " list of weight" + str(self.list_weight)

    def output(self, list_input):
        """
        :param list_input: a list of input (numbers). This list length should be the nbr_input entered at the creation
        :return: a positive number calculated with the input
        """
        if len(list_input) != len(self.list_weight):
            print("list_input and list_weight don't have the same length\n" +
                  'The neuron : ' + str(self) + " ; The input : " + str(list_input))
            return None
        res = 0
        for i in range(len(self.list_weight)):
            res += self.list_weight[i] * list_input[i]
        return 1 / (1 + exp(-res))

    def mutation(self):
        """
        Change randomly one weight on the list_weight
        """
        i = randrange(len(self.list_weight))
        self.list_weight[i] = Neuron.random_weight()

    @staticmethod
    def random_weight():
        """
        :return: a random weight
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


class Bot:
    """
    This is a bot.
    """
    def __init__(self, list_neuron, i, j):
        self.list_neuron = list_neuron
        self.i = i
        self.j = j
        self.strength = 0
        self.list_input = [0 for i in range(8)]
        self.list_output = [0, 0, 0, 0]  # up / down / left / right
        self.sprite = None

    def __str__(self):
        return "id : " + str(id(self)) + " position : i = " + str(self.i) + " ; j = " + str(
            self.j) + "Strength : " + str(self.strength) + "\n Neurons : " + str(self.list_neuron)

    def display(self):
        """
        Display the bot at the position i;j on the canvas (canvas should be a global variable
        :return:
        """
        canvas.delete(self.sprite)
        self.sprite = canvas.create_oval(self.i * square_size, self.j * square_size,
                                         (self.i + 1) * square_size, (self.j+1) * square_size,
                                         fill=self.int_to_color(self.strength))

    @staticmethod
    def int_to_color(strength):
        """
        :param strength: a number between 0 and max_strength
        :return: a string like "#RRGGBB" which can be interpreted as a color
        (the more strength is high the reder is the color)
        """
        red = strength * 255 // max_strength
        blue = 255 - red
        green = 0
        res = "#"
        for i in [red, green, blue]:
            if i < 16:
                res += "0"+hex(i)[-1:].upper()
            else:
                res += hex(i)[-2:].upper()
        return res

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
        Calculate each output of the neurons and
        set list_output as the proper value.
        """
        temp_inputs = self.list_input[:]  # Copy the list
        temp_outputs = []
        for i_layer in range(len(self.list_neuron)):
            # for each layer of neurons
            for i_neuron in range(len(self.list_neuron[i_layer])):
                # for each neuron in this layer
                temp_outputs.append(self.list_neuron[i_layer][i_neuron].output(temp_inputs))
                # we add to temp_outputs the output of the neuron self.list_neuron[i_layer][i_neuron]
                # with temp_inputs as inputs
            temp_inputs = temp_outputs[:]
            temp_outputs = []
        self.list_output = temp_inputs[:]
        print(self.list_output)

    def move(self):
        """
        Check which out put is the "most activated" (which is higher) and move in that direction
        :return:
        """
        i_max = max_index(self.list_output)
        if i_max == 0 and self.j > 0:
            self.j -= 1
        elif i_max == 1 and self.j < height-1:
            self.j += 1
        elif i_max == 2 and self.i > 0:
            self.i -= 1
        elif i_max == 3 and self.i < width-1:
            self.i += 1

    def eat(self, list_bot, list_gem, list_dead_bot):
        """
        Check if there is a weaker foe or a Gem at my location, if so, eat it!
        """
        gem = Gem.detect_gem(self.i, self.j, list_gem)
        if gem is not None:
            if self.strength < max_strength:
                self.strength += 1
            gem.erase()
            list_gem.remove(gem)
        foe = self.detect_foe(self.i, self.j, list_bot)
        if foe is not None:
            if self.strength+5 <= max_strength:
                self.strength += 5
            foe.erase()
            list_dead_bot.append(foe)
            list_bot.remove(foe)


class Gem:
    """
    This is a gem
    """
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.rayon = 3
        self.sprite = canvas.create_oval(self.i * square_size, self.j * square_size,
                                         (self.i + 1) * square_size, (self.j+1) * square_size, fill='green')

    def erase(self):
        """
        Erase the sprite from the canvas
        """
        canvas.delete(self.sprite)

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


# Genetic Algorithm
def selection(nbr_to_choose):
    """
    Add list_dead bot to list_bot, then select the nbr_to_choose best
    :param nbr_to_choose: the number of bot to choose
    :return: the list of the nbr_to_choose best bot
    """
    global list_bot
    list_bot += list_dead_bot
    bot_sort()
    return list_bot[:nbr_to_choose]


def mate(best):
    """
    Mate the best bot with each other
    :param best: the bots to mate
    :return: the list of the bots created
    """
    res = []
    for k in range(len(best)//2):
        for i in range(len(best)):
            temp = randrange(0, len(best))
            while temp != i:
                temp = randrange(0, len(best))
            res.append(crossover(best[i], best[temp]))
    return res


def crossover(bot1, bot2):
    """
    Create a new bot with the crossover and the mutation method
    :param bot1:
    :param bot2:
    :return: a new bot
    """
    list_neuron = [[], []]
    for i_layer in range(len(bot1.list_neuron)):
        nbr_bot1 = 0
        nbr_bot2 = 0
        for i_neuron in range(len(bot1.list_neuron[i_layer])):
            tau = (len(bot1.list_neuron[i_layer])/2 - nbr_bot1) / (len(bot1.list_neuron[i_layer]) - (nbr_bot1 + nbr_bot2))
            p = random()
            if p > tau:
                list_neuron[i_layer] += [bot2.list_neuron[i_layer][i_neuron]]
                nbr_bot2 += 1
            else:
                list_neuron[i_layer] += [bot1.list_neuron[i_layer][i_neuron]]
                nbr_bot1 += 1
            if random() < 1/9:
                neuron = list_neuron[i_layer][i_neuron]
                neuron.mutation()     # Attention mutation
    bot3 = Bot(list_neuron, randrange(width), randrange(height))
    return bot3


def bot_sort():
    """
    sort the global list list_bot with strength increasing
    """
    global list_bot
    for i in range(len(list_bot)-1):
        if list_bot[i].strength < list_bot[i+1].strength:
            list_bot[i], list_bot[i + 1] = list_bot[i + 1], list_bot[i]
            temp = i
            while temp > 0 and list_bot[temp].strength > list_bot[temp-1].strength:
                list_bot[temp], list_bot[temp - 1] = list_bot[temp - 1], list_bot[temp]
                temp -= 1


# Useful stuff
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


# Generate a new level
def list_neuron_random(nbr_input, list_nbr_neurons):
    """
    Create a list of two list of neurons
    :param nbr_input: the number of inputs for the neuron on the first layer
    :param list_nbr_neurons: the list of with the number of neuron we want in the layer i in list_nbr_neurons[i]
    :return: the list of list of neurons
    """
    res = [[] for i in range(len(list_nbr_neurons))]
    for i_layer in range(len(res)):
        for i_neuron in range(list_nbr_neurons[i_layer]):
            res[i_layer].append(Neuron(nbr_input))
        nbr_input = len(res[i_layer])   # Now the nbr_input is the number of neurons in the previous layer
    return res


def generate_gem(list_gem):
    """
    erase list_gem then generate nbr_gems Gems and puts them in list_gems
    """
    for gem in list_gem:
        gem.erase()
    list_gem.clear()
    for i in range(nbr_gems):
        list_gem.append(Gem(randrange(width), randrange(height)))

def trigger_new_generation():
    new_generation(list_bot, list_gem, list_dead_bot);

def new_generation(list_bot, list_gem, list_dead_bot):
    """
    Select the best from this generation
    Erase the old bots
    create the new bots
    and generate the gems
    """
    best = selection(7)
    for bot in list_bot:
        bot.erase()
    list_bot.clear()
    for bot in mate(best):
        list_bot.append(bot)
    list_dead_bot.clear()
    generate_gem(list_gem)


# Global Variables
width = 60      # in square
height = 60     # in square
square_size = 10
nbr_gems = 100
fps = 30
max_strength = 30

# Creation of the graphic interface
root = tk.Tk()
canvas = tk.Canvas(root, width=width*square_size, height=height*square_size, background='white')
canvas.pack(side="top")
quit_button = tk.Button(root, text="QUIT", fg="red", command=root.destroy)
quit_button.pack()
generation_button = tk.Button(root, text="New Generation", command=trigger_new_generation)
generation_button.pack()


# Main
def trigger_main():
    main(list_bot, list_gem, list_dead_bot)


def main(list_bot, list_gem, list_dead_bot):
    """
    update the bots in list_bot
    make them eat
    and relaunch the function main after a little time
    """
    for bot in list_bot:
        bot.update(list_bot, list_gem)
    for bot in list_bot:
        bot.eat(list_bot, list_gem, list_dead_bot)
    root.after(1000 // fps, trigger_main)


if __name__ == '__main__':
    list_bot = []
    list_dead_bot = []
    list_gem = []
    generate_gem(list_gem)
    for i in range(28):
        list_bot.append(Bot(list_neuron_random(8,[4]), randrange(width), randrange(height)))
    main(list_bot, list_gem, list_dead_bot)
    root.mainloop()
