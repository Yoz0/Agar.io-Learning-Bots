import tkinter as tk
from bot import bot_sort
from botv1 import BotV1
from gem import Gem
from random import randrange
from copy import deepcopy
from config import *


class GameV1:
    def __init__(self):
        self.file_res = open("res.data", 'w')
        self.file_net = open("net.data", 'w')

        self.init_UI()

        self.generation = 1
        self.turn = 0       # counts the number of frames passed since a new generation
        self.auto_gen = 1   # 1 if the generations shall pass automatically
        self.speed = DEFAULT_SPEED    # speed of time

        # init gems
        self.list_gem = []
        self.list_gem_sprite = []
        self.generate_gem()

        # init bots
        self.list_bot = []
        self.list_bot_sprite = []
        for i in range(NBR_BOT):
            self.list_bot.append(BotV1.quick_init(self.canvas, name=str(self.generation) + "th_gen_" + str(i)))
        self.place_bots_in_line()

        self.list_dead_bot = []

        # tell tk to launch trigger_game in a while
        self.root.after(1000 // self.speed, self.game)

        self.root.mainloop()

    def game(self):
        """
        Updates the bots in 'list_bot'.
        Calls 'eat()' for each of them.
        And relaunches 'game()' after a little time.

        :param entry_speed: tkinter object of type Entry, the field that gives the
                             speed of time.
        """

        self.turn += 1
        for bot in self.list_bot:
            bot.update(self.list_bot, self.list_gem)
        # for bot in self.list_bot:
        #    bot.eat(self.list_bot, self.list_gem, self.list_dead_bot)
        self.collision()
        if self.turn > NB_TURN_GENERATION and self.auto_gen == 1:
            self.new_generation()

        self.update_speed()

        self.root.after(1000 // self.speed, self.game)

    def new_generation(self):
        """
        Creates a new set of bots from the best ones of this generation and
        resets the board for the bot of the next gen to play with. The mean strengh
        of the best bots of the current generation is saved in the file 'self.file_res'.
        """
        self.generation += 1
        self.turn = 0

        nbr_alive = len(self.list_bot)
        nbr_gems_remaining = len(self.list_gem)

        self.list_bot += self.list_dead_bot
        self.list_dead_bot.clear()

        # remove everyone from display
        for bot in self.list_bot:
            bot.erase()

        # select the best NB_SELECT_BOT
        best = self.selection()
        self.gen_info(best, nbr_alive, nbr_gems_remaining)

        self.list_bot.clear()

        # mate the best bots
        mating_list = self.get_mating_list(best)

        # crossover the bots
        for i, (b1, b2) in enumerate(mating_list):
            self.list_bot.append(b1.mate_with(b2, str(self.generation) + "th_gen_" + str(i)))

        self.generation_text.configure(text="Generation : " + str(self.generation))
        self.generation_text.update()

        self.generate_gem()

        self.place_bots_in_line()

    def collision(self):
        for bot1 in self.list_bot:
            for bot2 in self.list_bot:
                if bot1 != bot2 and bot1.i == bot2.i and bot1.j == bot2.j:
                    self.collide_bot_bot(bot1, bot2)
            for gem in self.list_gem:
                if bot1.i == gem.i and bot1.j == gem.j:
                    self.collide_bot_gem(bot1, gem)

    def collide_bot_bot(self, bot1, bot2):
        if bot1.strength < bot2.strength:
            bot1.erase()
            self.list_bot.remove(bot1)
            self.list_dead_bot.append(bot1)
            bot2.inc_strength(5)
        elif bot1.strength > bot2.strength:
            bot2.erase()
            self.list_bot.remove(bot2)
            self.list_dead_bot.append(bot2)
            bot1.inc_strength(5)
        else:
            pass

    def collide_bot_gem(self, bot, gem):
        gem.erase()
        self.list_gem.remove(gem)
        bot.inc_strength(1)

    def gen_info(self, best, nbr_alive, nbr_gems_remaining):
        print("\nbest bots :")
        for bot in best:
            print(str(bot))

        #calculate mean
        sum = 0
        for bot in best:
            sum += bot.strength

        mean = sum/NB_SELECT_BOT
        alive_percent = (nbr_alive/NBR_BOT)*100
        gems_eaten_percent = ((NBR_GEMS-nbr_gems_remaining)/NBR_GEMS)*100

        print("Mean strength: " + str(mean))
        print("Remaining alive bots: " + str(alive_percent) + "%")
        print("Gems eaten: " + str(gems_eaten_percent) + "%")
        self.file_res.write(str(mean) + " " +
                       str(alive_percent) + " " +
                       str(gems_eaten_percent) + "\n")

    def selection(self):
        """
        Sorts 'self.list_bots' and returns a list with the 'NB_SELECT_BOT' best bots.
        :return: the list of the 'NB_SELECT_BOT' best bot

        warning : this function will have for side effect to sort the actual list
                  'self.list_bots'!!
                  The returned list is a list of references to the bots that are in
                  self.list_bot!
        """
        bot_sort(self.list_bot)
        return self.list_bot[:NB_SELECT_BOT]

    def init_UI(self):
        #root app
        self.root = tk.Tk()

        #game frame
        self.canvas = tk.Canvas(self.root, width=WIDTH*SQUARE_SIZE, height=HEIGHT*SQUARE_SIZE, background='white')
        self.canvas.pack(side="top")

        #left and right containers
        self.frame_left = tk.Frame(self.root)
        self.frame_left.pack(side = "left")
        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side = "right")

        #left widgets
        self.quit_button = tk.Button(self.frame_left, text="QUIT", fg="red", command=self.quit)
        self.quit_button.pack()
        self.generation_button = tk.Button(self.frame_left, text="New Generation", command=self.new_generation)
        self.generation_button.pack()
        self.generation_text = tk.Label(self.frame_left, text="Generation : 1")
        self.generation_text.pack()

        #right widgets
        self.save_net = tk.Button(self.frame_right, text="save neural network", command=self.save_net)
        self.save_net.pack()
        self.auto_pass_generation = tk.Checkbutton(self.frame_right, text="disable automatic generations", command=self.toggle_auto_gen)
        self.auto_pass_generation.pack()

        #middle widgets
        self.speed_text = tk.Label(text="Speed")
        self.speed_text.pack()
        self.entry_speed = tk.Entry(self.root)
        self.entry_speed.pack()
        self.entry_speed.delete(0, tk.END)
        self.entry_speed.insert(0, str(DEFAULT_SPEED))

    def generate_gem(self):
        """
        Erases 'self.list_gem', generates 'NBR_GEMS' Gems and puts them in 'list_gem'.
        """
        for gem in self.list_gem:
            gem.erase()
        self.list_gem.clear()
        for i in range(NBR_GEMS):
            self.list_gem.append(Gem(randrange(WIDTH), randrange(HEIGHT), self.canvas))

    def place_bots_in_line(self):
        """
        Changes the position of every robot in 'self.list_bot', so that they form
        a line in the bottom of the board.
        """
        if len(self.list_bot) > WIDTH/2:
            raise ValueError("too many bots to do that\n")

        for i, bot in enumerate(self.list_bot):
            bot.i = 2*i
            bot.j = HEIGHT-1

    def update_speed(self):
        self.speed = self.entry_speed.get()

        if self.speed == "":
            self.speed = "1"

        self.speed = int(self.speed)
        if self.speed <= 0:
            self.speed = 1

    def get_mating_list(self, best):
        """
        Given a list of bots, this function creates a random mating list
        of length 'NBR_BOT'. Each item of the list is a tuple of two bots from 'best'
        to crossover. Each bot from 'best' mates at least 'NBR_BOT//len(best)' times.
        The number 'NBR_BOT//len_best' is the number of times you have to make
        each bot mate in order to have a mating list of size 'NBR_BOT'.
        :param best: the bots to mate
        :return: the list of bots to crossover of length 'NBR_BOT'.
        """
        len_best = len(best)
        res = []
        for k in range(len_best):
            for i in range(NBR_BOT//len_best):
                temp = randrange(0, len_best)
                while temp == k:
                    temp = randrange(0, len_best)
                res.append((best[k], best[temp]))
        return res

    def toggle_auto_gen(self):
        self.auto_gen = not self.auto_gen

    def save_net(self):
        i = randrange(len(self.list_bot))
        self.file_net.write(str(self.list_bot[i].brain))
        print("The neural net of a bot randomly choosen has been saved.")

    def quit(self):
        self.file_res.close()
        self.file_net.close()
        self.root.destroy()

    # def display_gem(self):
    #     for sprite in self.list_gem_sprite:
    #         self.canvas.delete(sprite)
    #     self.list_gem_sprite.clear()

    #     for gem in self.list_gem:
    #         self.list_gem_sprite.append(
    #             self.canvas.create_rectangle(
    #                 self.i * SQUARE_SIZE + MARGE,
    #                 self.j * SQUARE_SIZE + MARGE,
    #                 (self.i + 1) * SQUARE_SIZE - MARGE,
    #                 (self.j+1) * SQUARE_SIZE - MARGE,
    #                 fill=random_color()
    #             )
    #         )

    # def display_bot(self):

