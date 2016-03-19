from random import random, randrange


from config import *
from neuron import *
from bot import *
from gem import *

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
            while temp == i:
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
    bot3 = Bot(list_neuron, randrange(WIDTH), randrange(HEIGHT))
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
    erase list_gem then generate NBR_GEMS Gems and puts them in list_gems
    """
    for gem in list_gem:
        gem.erase()
    list_gem.clear()
    for i in range(NBR_GEMS):
        list_gem.append(Gem(randrange(WIDTH), randrange(HEIGHT)))

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
    root.after(1000 // FPS, trigger_main)

# Creation of the graphic interface
quit_button = tk.Button(root, text="QUIT", fg="red", command=root.destroy)
quit_button.pack()
generation_button = tk.Button(root, text="New Generation", command=trigger_new_generation)
generation_button.pack()

if __name__ == '__main__':
    list_bot = []
    list_dead_bot = []
    list_gem = []
    generate_gem(list_gem)
    for i in range(NBR_BOT):
        list_bot.append(Bot(list_neuron_random(8,[4]), randrange(WIDTH), randrange(HEIGHT)))
    main(list_bot, list_gem, list_dead_bot)
    root.mainloop()
