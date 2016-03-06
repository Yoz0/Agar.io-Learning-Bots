from math import exp
from random import random, randrange
import tkinter as tk


class Neuron:
    def __init__(self, nbr_input):
        self.list_weight = Neuron.list_weight_random(nbr_input)

    def __str__(self):
        return "id : " + str(id(self)) + " list of weight" + str(self.list_weight)

    def output(self, list_input):
        if len(list_input) != len(self.list_weight):
            print("list_input and list_weight don't have the same length\n" +
                  'The neuron : ' + str(self) + " ; The inputs : " + str(list_input))
            return None
        res = 0
        for i in range(len(self.list_weight)):
            res += self.list_weight[i] * list_input[i]
        return 1 / (1 + exp(-res))

    def mutation(self):
        i = randrange(len(self.list_weight))
        self.list_weight[i] = Neuron.random_weight()

    @staticmethod
    def random_weight():
        return random()*2-1

    @staticmethod
    def list_weight_random(nbr_input):
        res = []
        for i in range(nbr_input):
            res.append(Neuron.random_weight())
        return res


class Bot:
    def __init__(self, list_neuron, i, j):
        self.list_neuron = list_neuron
        self.i = i
        self.j = j
        self.strength = 1
        self.list_input = [0 for i in range(8)]
        self.list_output = [0, 0, 0, 0]  # up / down / left / right
        self.sprite = canvas.create_oval(self.i * square_size, self.j * square_size,
                                         (self.i + 1) * square_size, (self.j+1) * square_size,
                                         fill=int_to_color(self.strength))

    def __str__(self):
        return "id : " + str(id(self)) + " position : i = " + str(self.i) + " ; j = " + str(
            self.j) + "Strength : " + str(self.strength) + "\n Neurons : " + str(self.list_neuron)

    def display(self):
        canvas.delete(self.sprite)
        self.sprite = canvas.create_oval(self.i * square_size, self.j * square_size,
                                         (self.i + 1) * square_size, (self.j+1) * square_size,
                                         fill=int_to_color(self.strength))

    def erase(self):
        canvas.delete(self.sprite)

    def update(self):
        self.update_input()
        self.update_output()
        self.move()
        self.display()

    def update_input(self):
        self.list_input = [0 for k in range(8)]
        if Gem.detect_gem(self.i, self.j - 1) is not None:
            self.list_input[0] = 1
        if Gem.detect_gem(self.i, self.j + 1) is not None:
            self.list_input[1] = 1
        if Gem.detect_gem(self.i - 1, self.j) is not None:
            self.list_input[2] = 1
        if Gem.detect_gem(self.i + 1, self.j) is not None:
            self.list_input[3] = 1
        foe = self.detect_foe(self.i, self.j - 1)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[4] = 1
            else:
                self.list_input[4] = -1
        foe = self.detect_foe(self.i, self.j + 1)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[5] = 1
            else :
                self.list_input[5] = -1
        foe = self.detect_foe(self.i - 1, self.j)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[6] = 1
            else :
                self.list_input[6] = -1
        foe = self.detect_foe(self.i + 1, self.j)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[7] = 1
            else :
                self.list_input[7] = -1

    def detect_foe(self, i, j):
        k = 0
        while k < len(list_bot):
            foe = list_bot[k]
            if foe.i == i and foe.j == j and self != foe:
                return foe
            k += 1
        return None

    def update_output(self):
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

    def move(self):
        i_max = max_index(self.list_output)
        if i_max == 0 and self.j > 0:
            self.j -= 1
        elif i_max == 1 and self.j < height-1:
            self.j += 1
        elif i_max == 2 and self.i > 0:
            self.i -= 1
        elif i_max == 3 and self.i < width-1:
            self.i += 1

    def eat(self):
        gem = Gem.detect_gem(self.i, self.j)
        if gem is not None:
            if self.strength < max_strength:
                self.strength += 1
            gem.erase()
            list_gem.remove(gem)
        foe = self.detect_foe(self.i, self.j)
        if foe is not None:
            if self.strength+5 <= max_strength:
                self.strength += 5
            foe.erase()
            list_dead_bot.append(foe)
            list_bot.remove(foe)


class Gem:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.rayon = 3
        self.sprite = canvas.create_oval(self.i * square_size, self.j * square_size,
                                         (self.i + 1) * square_size, (self.j+1) * square_size, fill='green')

    def erase(self):
        canvas.delete(self.sprite)

    @staticmethod
    def detect_gem(i, j):
        k = 0
        while k < len(list_gem):
            gem = list_gem[k]
            if gem.i == i and gem.j == j:
                return gem
            k += 1
        return None


# Genetic Algorithm
def selection():
    global list_bot
    list_bot += list_dead_bot
    bot_sort()
    return list_bot[:7]


def mate(best):
    res = []
    for k in range(4):
        for i in range(len(best)):
            temp = randrange(0, len(best))
            while temp != i:
                temp = randrange(0,len(best))
            res.append(crossover(best[i], best[temp]))
    return res


def crossover(bot1, bot2):
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
    i_max = 0
    maxi = - float('inf')
    for i in range(len(list_int)):
        if list_int[i] > maxi:
            i_max = i
            maxi = list_int[i]
    return i_max


def int_to_color(strength):
    strength *= 30
    if strength < 16:
        return "#FFFF0"+hex(strength)[-1:]
    else:
        return "#FFFF"+hex(strength)[-2:]


# Generate a new level
def list_neuron_random(nbr_inputs, nbr_neurones_cache, nbr_neurones_cache_2):
    res = [[], []]
    for j in range(nbr_neurones_cache):
        res[0] += [Neuron(nbr_inputs)]
    for j in range(nbr_neurones_cache_2):
        res[1] += [Neuron(nbr_neurones_cache)]
    return res


def generate_gem():
    global list_gem
    for gem in list_gem:
        gem.erase()
    list_gem = []
    for i in range(nbr_gems):
        list_gem.append(Gem(randrange(width), randrange(height)))


def new_generation():
    global list_bot
    best = selection()
    for bot in list_bot:
        bot.erase()
    list_bot = mate(best)
    generate_gem()


def start():
    global list_bot
    for bot in list_bot:
            bot.erase()
    list_bot = []
    generate_gem()
    for i in range(28):
        list_bot.append(Bot(list_neuron_random(8, 8, 4), randrange(width), randrange(height)))

# Global Variables
width = 60      # in square
height = 60     # in square
square_size = 10
list_bot = []
list_dead_bot = []
list_gem = []
nbr_gems = 100
fps = 30
max_strength = 30

# Creation of the graphic interface
root = tk.Tk()
canvas = tk.Canvas(root, width=width*square_size, height=height*square_size, background='white')
canvas.pack(side="top")
quit_button = tk.Button(root, text="QUIT", fg="red", command=root.destroy)
quit_button.pack()
generation_button = tk.Button(root, text="New Generation", command=new_generation)
generation_button.pack()


# Main
def main():
    for bot in list_bot:
        bot.update()
    for bot in list_bot:
        bot.eat()
    root.after(1000 // fps, main)

restart_button = tk.Button(root, text="Restart", command=start)
restart_button.pack()

if __name__ == '__main__':
    start()
    main()
    root.mainloop()
