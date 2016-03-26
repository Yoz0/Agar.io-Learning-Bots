from random import random, randrange
from copy import *
from config import *
from neuron import *
from bot import *
from gem import *


# Genetic Algorithm
def selection(list_of_bots, nbr_to_choose):
    """
    Sorts 'list_of_bots' and returns a list with the 'nbr_to_choose' best bots.
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


def get_mating_list(best, nbr_to_make):
    """
    Given a list of bots, this function creates a random mating list
    of length 'nbr_to_make'. Each item of the list is a tuple of two bots from 'best'
    to crossover. Each bot from 'best' mates at least 'nbr_to_make//len(best)' times.
    The number 'nbr_to_make//len_best' is the number of times you have to make
    each bot mate in order to have a mating list of size 'nbr_to_make'.
    :param best: the bots to mate
    :return: the list of bots to crossover of length 'nbr_to_make'.
    """
    len_best = len(best)
    res = []
    for k in range(len_best):
        for i in range(nbr_to_make//len_best):
            temp = randrange(0, len_best)
            while temp == k:
                temp = randrange(0, len_best)
            res.append((best[k], best[temp]))
    return res


def bot_sort(list_of_bots):
    """
    Sorts 'list_bot' with strength decreasing.
    :param list_of_bots: list of bots to sort
    """
    for i in range(len(list_of_bots)-1):
        if list_of_bots[i].strength < list_of_bots[i+1].strength:
            list_of_bots[i], list_of_bots[i + 1] = list_of_bots[i + 1], list_of_bots[i]
            temp = i
            while temp > 0 and list_of_bots[temp].strength > list_of_bots[temp-1].strength:
                list_of_bots[temp], list_of_bots[temp - 1] = list_of_bots[temp - 1], list_of_bots[temp]
                temp -= 1


# Generate a new level
def generate_gem(list_gem):
    """
    Erases 'list_gem', generates 'NBR_GEMS' Gems and puts them in 'list_gem'.
    """
    for gem in list_gem:
        gem.erase()
    list_gem.clear()
    for i in range(NBR_GEMS):
        list_gem.append(Gem(randrange(WIDTH), randrange(HEIGHT)))


def place_bots_in_line(list_of_bots):
    """
    Changes the position of every robot in 'list_of_bots', so that they form
    a line in the bottom of the board.
    """
    if len(list_of_bots) > WIDTH/2:
        raise ValueError("too many bots to do that\n")

    for i, bot in enumerate(list_of_bots):
        bot.i = 2*i
        bot.j = HEIGHT-1


def trigger_new_generation():
    global list_bot
    global list_gem
    global list_dead_bot
    new_generation(list_bot, list_gem, list_dead_bot)


def new_generation(list_bot, list_gem, list_dead_bot):
    """
    Creates a new set of bots from the best ones of this generation and
    resets the board for the bot of the next gen to play with. The mean strengh
    of the best bots of the current generation is saved in the file 'FILE_RES'.
    """
    global turn
    global generation

    nbr_alive = len(list_bot)
    nbr_gems_remaining = len(list_gem)

    #gather every bot
    list_bot += list_dead_bot

    #empty list of dead bots
    list_dead_bot.clear()

    #remove everyone from display
    for bot in list_bot:
        bot.erase()

    #select the best NB_SELECT_BOT
    best = selection(list_bot, NB_SELECT_BOT)
    print("\nbest bots :")
    for bot in best:
        print(str(bot))
        #calculate and print mean
    sum = 0
    for bot in best:
        sum += bot.strength

    mean = sum/NB_SELECT_BOT
    alive_percent = (nbr_alive/NBR_BOT)*100 
    gems_eaten_percent = ((NBR_GEMS-nbr_gems_remaining)/NBR_GEMS)*100
    print("Mean strength: " + str(mean))
    print("Remaining alive bots: " + str(alive_percent) + "%")
    print("Gems eaten: " + str(gems_eaten_percent) + "%")
    FILE_RES.write(str(mean) + " " +
                   str(alive_percent) + " " +
                   str(gems_eaten_percent) + "\n")

    #clear the list_bot
    list_bot.clear()

    #mate the best bots
    mating_list = get_mating_list(best, NBR_BOT)

    #crossover the bots
    generation += 1
    for i, (b1, b2) in enumerate(mating_list):
        list_bot.append(b1.mate_with(b2, str(generation) + "th_gen_" + str(i)))

    generation_text.configure(text="Generation : " + str(generation))
    generation_text.update()
    turn = 0

    #generate a new set of gems
    generate_gem(list_gem)

    place_bots_in_line(list_bot)


def trigger_bring_to_life():
    global list_bot
    global list_dead_bot
    bring_to_life(list_bot, list_dead_bot)


def bring_to_life(list_bot, list_dead_bot):
    """
    This function will bring every bot to life, and replace them on the bottom side.
    It will not reset their strength ! The purpose of this function is to let
    more time to bots to prove their value before selecting them.
    """
    list_bot += list_dead_bot
    list_dead_bot.clear()
    place_bots_in_line(list_bot)
    for bot in list_bot:
        bot.erase()


def trigger_more_gems():
    global list_gem
    more_gems(list_gem)


def more_gems(list_gem):
    """Adds 100 gems randomly on the field"""
    for i in range(100):
        list_gem.append(Gem(randrange(WIDTH), randrange(HEIGHT)))


def trigger_reset_gems():
    global list_gem
    generate_gem(list_gem)


def trigger_another_chance():
    """Same as 'bring_to_life()', but reset gems too."""
    global list_gem
    global list_bot
    global list_dead_bot
    generate_gem(list_gem)
    bring_to_life(list_bot, list_dead_bot)


def toggle_auto_gen():
    global auto_gen
    auto_gen = not auto_gen


# Main
def trigger_game():
    global list_bot
    global list_gem
    global list_dead_bot
    global entry_speed
    game(list_bot, list_gem, list_dead_bot, entry_speed)

def game(list_bot, list_gem, list_dead_bot, entry_speed):
    """
    Updates the bots in 'list_bot'.
    Calls 'eat()' for each of them.
    And relaunches 'game()' after a little time.

    :param entry_speed: tkinter object of type Entry, the field that gives the
                         speed of time.
    """
    global turn
    global auto_gen

    turn += 1
    for bot in list_bot:
        bot.update(list_bot, list_gem)
    for bot in list_bot:
        bot.eat(list_bot, list_gem, list_dead_bot)

    if turn > NB_TURN_GENERATION and auto_gen == 1:
        trigger_new_generation()

    speed = entry_speed.get()

    if speed == "":
        speed = "1"

    speed = int(speed)
    if speed < 0:
        speed = 1

    root.after(1000 // speed, trigger_game)

# Creation of the graphic interface
frame_left = tk.Frame(root)
frame_left.pack(side = "left")
frame_right = tk.Frame(root)
frame_right.pack(side = "right")

quit_button = tk.Button(frame_left, text="QUIT", fg="red", command=root.destroy)
quit_button.pack()
generation_button = tk.Button(frame_left, text="New Generation", command=trigger_new_generation)
generation_button.pack()
button_bring_to_life = tk.Button(frame_right, text="Bring everyone to life", command=trigger_bring_to_life)
button_bring_to_life.pack()
button_more_gems = tk.Button(frame_right, text="MOAR GEMS", command=trigger_more_gems)
button_more_gems.pack()
button_reset_gems = tk.Button(frame_right, text="reset gems", command=trigger_reset_gems)
button_reset_gems.pack()
button_another_chance = tk.Button(frame_left, text="another chance", command=trigger_another_chance)
button_another_chance.pack()
generation_text = tk.Label(frame_left, text="Generation : 1")
generation_text.pack()
auto_pass_generation = tk.Checkbutton(frame_right, text="disable automatic generations", command=toggle_auto_gen)
auto_pass_generation.pack()
# slider_speed = tk.Scale(root, label="speed", from_=1, to=600, orient=tk.HORIZONTAL)
# slider_speed.pack()
# slider_speed.set(30)
speed_text = tk.Label(text="Speed")
speed_text.pack()
entry_speed = tk.Entry(root)
entry_speed.pack()
entry_speed.delete(0, tk.END)
entry_speed.insert(0, str(FPS))

if __name__ == '__main__':
    generation = 1
    turn = 0
    auto_gen = 1
    list_bot = []
    list_dead_bot = []
    list_gem = []
    generate_gem(list_gem)
    for i in range(NBR_BOT):
        list_bot.append(Bot.quick_init(name=str(generation) + "th_gen_" + str(i)))
    place_bots_in_line(list_bot)
    game(list_bot, list_gem, list_dead_bot, entry_speed)
    root.mainloop()
    FILE_RES.close()
