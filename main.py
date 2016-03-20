from random import random, randrange
from copy import *

from config import *
from neuron import *
from bot import *
from gem import *

# Genetic Algorithm
def selection(list_of_bots, nbr_to_choose):
    """
    Sorts 'list_of_bots' and return a list with the 'nbr_to_choose' best bots
    :param list_of_bots: list of bots from which to select
    :param nbr_to_choose: the number of bot to choose
    :return: the list of the 'nbr_to_choose' best bot

    warning : this function will have for side effect to sort the list actual list
              given in argument !!
              The returned list, however, is completly independent from the one given
              in argument !
    """

    bot_sort(list_of_bots)
    return deepcopy(list_of_bots[:nbr_to_choose])


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
    Create a new bot with the crossover
    :param bot1:
    :param bot2:
    :return: a new bot
    """
    list_layer = []
    for i_layer in range(len(bot1.brain)):
        list_neurons =[]
        nbr_neuron_from_bot1 = len(bot1.brain[i_layer])//2
        # We have to select nbr_neuron_from_bot1 integers in the sequence range(len(layer))
        index_of_neurons_from_bot_1 = []
        for i in range(nbr_neuron_from_bot1):
            index = randrange(len(bot1.brain[i_layer]))
            while index in index_of_neurons_from_bot_1:    # We don't want the same index twice
                index = randrange(len(bot1.brain[i_layer]))
            index_of_neurons_from_bot_1.append(index)
        for i in range(len(bot1.brain[i_layer])):
            if i in index_of_neurons_from_bot_1:
                list_neurons.append(deepcopy(bot1.brain[i_layer][i]))
            else:
                list_neurons.append(deepcopy(bot2.brain[i_layer][i]))
        layer = Layer(list_neurons)
        list_layer.append(layer)
    brain = Neural_network(list_layer)
    bot3 = Bot(brain.nbr_input, brain, randrange(WIDTH), randrange(HEIGHT))
    return bot3


def bot_sort(list_of_bots):
    """
    Sort the list 'list_of_bots' given in argument, with strength increasing
    """

    for i in range(len(list_of_bots)-1):
        if list_of_bots[i].strength < list_of_bots[i+1].strength:
            list_of_bots[i], list_of_bots[i + 1] = list_of_bots[i + 1], list_of_bots[i]
            temp = i
            while temp > 0 and list_of_bots[temp].strength > list_of_bots[temp-1].strength:
                list_of_bots[temp], list_of_bots[temp - 1] = list_of_bots[temp - 1], list_of_bots[temp]
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

def place_bots_in_line():
    global list_bot

    if len(list_bot) > WIDTH/2:
        raise ValueError("too many bots to do that\n")

    for i, bot in enumerate(list_bot):
        bot.i = 2*i
        bot.j = WIDTH-1

def trigger_new_generation():
    global list_bot
    global list_gem
    global list_dead_bot
    global generation
    new_generation(list_bot, list_gem, list_dead_bot, generation)

def new_generation(list_bot, list_gem, list_dead_bot, generation):
    """
    Select the best from this generation
    Erase the old bots
    create the new bots
    and generate the gems
    """

    # best = selection(7)

    # for bot in list_bot:
    #     bot.erase()
    # list_bot.clear()

    # for bot in mate(best):
    #     list_bot.append(bot)
    # list_dead_bot.clear()
    # generate_gem(list_gem)

    #gather every bot
    list_bot += list_dead_bot

    #empty list of dead bots
    list_dead_bot.clear()

    #remove everyone from display
    for bot in list_bot:
        bot.erase()

    list_bot.clear()
    #select the best NB_SELECT_BOT
    for b in selection(list_bot, NB_SELECT_BOT):
        #re-set the list of bots
        list_bot.append(b)

    print("\nchoosen bots :")
    for bot in list_bot:
        print(str(bot))

    #calculate and print mean
    sum = 0
    for bot in list_bot:
        sum += bot.strength
    print("mean: " + str(sum/NB_SELECT_BOT))

    #reset every bot that we have kept from the previous generation
    for bot in list_bot:
        bot.reset()

    #complete the new generation with fresh random bots
    generation += 1
    for i in range(NBR_BOT - NB_SELECT_BOT):
        list_bot.append(Bot(8, Neural_network([4], 8), randrange(WIDTH), randrange(HEIGHT), str(generation) + "th_gen_" + str(i)))

    #generate a new set of gems
    generate_gem(list_gem)

    place_bots_in_line()

# Main
def trigger_main():
    global list_bot
    global list_gem
    global list_dead_bot
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
quit_button.pack(side="right")
generation_button = tk.Button(root, text="New Generation", command=trigger_new_generation)
generation_button.pack(side="right")

if __name__ == '__main__':
    generation = 1
    list_bot = []
    list_dead_bot = []
    list_gem = []
    generate_gem(list_gem)
    for i in range(NBR_BOT):
        list_bot.append(Bot(8, Neural_network([4], 8), randrange(WIDTH), randrange(HEIGHT), "1st_gen_" + str(i)))
    place_bots_in_line()
    main(list_bot, list_gem, list_dead_bot)
    root.mainloop()
