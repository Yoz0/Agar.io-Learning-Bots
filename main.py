from math import cos, sin, radians, atan, degrees, exp
from random import random,randrange
import tkinter as tk


class Neurone:
    def __init__(self, liste_poids):
        self.liste_poids = liste_poids

    def __str__(self):
        return "id : " + str(id(self)) + " liste des poids" + str(self.liste_poids)

    def output(self, liste_inputs):
        if len(liste_inputs) != len(self.liste_poids):
            print('Il y a un problème les inputs n\'on pas la même taille que les poids\n' +
                  'Le neurone : ' + str(self) + "\n Les inputs : " + str(liste_inputs))
            return -1
        res = 0
        for i in range(len(self.liste_poids)):
            res += self.liste_poids[i] * liste_inputs[i]
        return 1 / (1 + exp(-res))

    def mutation(self):
        i = randrange(len(self.liste_poids))
        self.liste_poids[i] = random()


class Bot:
    def __init__(self, listes_neurones, x, y):
        self.neurones = listes_neurones
        self.x = x
        self.y = y
        self.rayon = 5
        self.speed = 1000  # en pixel / seconde
        # self.turn_angle = 180
        # self.direction = 0  # En radians entre 0 et 2pi
        self.enemi_delta_x = float("inf")
        self.enemi_delta_y = float("inf")
        self.gem_delta_x = float("inf")
        self.gem_delta_y = float("inf")
        self.enemi_delta_rayon = float("inf")
        self.liste_inputs = [self.gem_delta_x, self.gem_delta_y,
                             self.enemi_delta_x, self.enemi_delta_y, self.enemi_delta_rayon]
        self.liste_outputs = [0, 0, 0, 0]  # haut / bas / gauche / droite
        self.sprite = canvas.create_oval(self.x - self.rayon, self.y - self.rayon,
                                         self.x + self.rayon, self.y + self.rayon, fill='blue')

    def __str__(self):
        return "id : " + str(id(self)) + " position : x = " + str(self.x) + " ; y = " + str(
            self.y) + "\n Neurones : " + str(self.neurones)

    def afficher(self):
        canvas.delete(self.sprite)
        self.sprite = canvas.create_oval(self.x - self.rayon, self.y - self.rayon,
                                         self.x + self.rayon, self.y + self.rayon, fill='blue')

    def effacer(self):
        canvas.delete(self.sprite)

    def update(self):
        self.update_input()
        self.update_output()
        self.avancer()
        self.afficher()

    def update_input(self):
        self.detecter_collision_gem()
        self.detecter_collision_enemi()
        self.detecter_gem_plus_proche()
        self.detecter_enemi_plus_proche()
        self.liste_inputs = [self.gem_delta_x, self.gem_delta_y,
                             self.enemi_delta_x, self.enemi_delta_y, self.enemi_delta_rayon]

    def detecter_collision_gem(self):
        i = 0
        while i < len(liste_gems):
            diam = liste_gems[i]
            if (diam.x - self.x) ** 2 + (diam.y - self.y) ** 2 <= (self.rayon + diam.rayon)**2:
                self.rayon += 1
                diam.effacer()
                del liste_gems[i]
            i += 1

    def detecter_collision_enemi(self):
        i = 0
        while i < len(liste_bots):
            enemi = liste_bots[i]
            if (enemi.x - self.x) ** 2 + (enemi.y - self.y) ** 2 <= (self.rayon + enemi.rayon)**2 and\
                            enemi.rayon < self.rayon and\
                            self != enemi:
                self.rayon += enemi.rayon
                enemi.effacer()
                liste_bots_mort.append(enemi)
                del liste_bots[i]
            i += 1

    def update_output(self):
        temp_inputs = self.liste_inputs[:]  # Petit trick pour copier la liste
        temp_outputs = []
        for i_couche in range(len(self.neurones)):
            # Pour chaque couche neuronale
            for i_neurone in range(len(self.neurones[i_couche])):
                # Pour chaque neurone dans cette couche
                temp_outputs.append(self.neurones[i_couche][i_neurone].output(temp_inputs))
                # On insère dans temp_outputs l'output du neurone self.neurones[i_couche][i_neurone]
                # avec temp_inputs comme inputs
            temp_inputs = temp_outputs[:]
            temp_outputs = []
        self.liste_outputs = temp_inputs[:]

    def avancer(self):
        # Ancienne version
        # self.direction = (self.direction - self.liste_outputs[1] * 10 + self.liste_outputs[2] * 10) % 360
        # self.direction = atan(self.liste_outputs[1]/self.liste_outputs[0])
        # self.x += self.speed * cos(self.direction) / (fps * self.rayon )
        # self.y += self.speed * sin(self.direction) / (fps * self.rayon )

        i_max = indice_max(self.liste_outputs)
        if i_max == 0 and (self.y - (self.speed / (self.rayon * fps))) > 0:
            self.y -= self.speed / (self.rayon * fps)
        elif i_max == 1 and (self.y + (self.speed / (self.rayon * fps))) < height:
            self.y += self.speed / (self.rayon * fps)
        elif i_max == 2 and (self.x - (self.speed / (self.rayon * fps))) > 0:
            self.x -= self.speed / (self.rayon * fps)
        elif i_max == 3 and (self.x + (self.speed / (self.rayon * fps))) < width:
            self.x += self.speed / (self.rayon * fps)

    def detecter_gem_plus_proche(self):
        self.gem_delta_x = float("inf")
        self.gem_delta_y = float("inf")
        for gem in liste_gems:
            if (gem.x - self.x) ** 2 + (gem.y - self.y) ** 2 < (self.gem_delta_x ** 2 + self.gem_delta_y ** 2):
                self.gem_delta_x = (gem.x - self.x)
                self.gem_delta_y = (gem.y - self.y)

    def detecter_enemi_plus_proche(self):
        self.enemi_delta_x = float("inf")
        self.enemi_delta_y = float("inf")
        for enemi in liste_bots:
            if (enemi.x - self.x) ** 2 + (enemi.y - self.y) ** 2 < (
                    self.enemi_delta_x ** 2 + self.enemi_delta_y ** 2) and self != enemi:
                self.enemi_delta_x = (enemi.x - self.x)
                self.enemi_delta_y = (enemi.y - self.y)
                self.enemi_delta_rayon = enemi.rayon - self.rayon


class Gem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rayon = 3
        self.sprite = canvas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon,
                                         self.y + self.rayon, fill='green')

    def effacer(self):
        canvas.delete(self.sprite)

def nouvelle_generation():
    global liste_bots, liste_gems
    for diam in liste_gems:
        diam.effacer()
    liste_gems = []
    best = selection()
    for bot in liste_bots:
        bot.effacer()
    liste_bots = accoupler(best)
    for i in range(nbr_gems):
        liste_gems.append(Gem(random() * width, random() * height))




def selection():
    trie_bot()
    return liste_bots[:7]

def accoupler(best):
    res = []
    for k in range(4):
        for i in range(len(best)):
            temp = randrange(0,len(best))
            while temp != i:
                temp = randrange(0,len(best))
            res.append(crossover(best[i], best[temp]))
    return res


def crossover(bot1,bot2):
    listes_neurones=[[],[]]
    for i_couche in range(len(bot1.neurones)):
        nbr_bot1 = 0
        nbr_bot2 = 0
        for i_neurone in range(len(bot1.neurones[i_couche])):
            tau = (len(bot1.neurones[i_couche])/2 - nbr_bot1) / (len(bot1.neurones[i_couche]) - (nbr_bot1 + nbr_bot2))
            p = random()
            if p > tau:
                listes_neurones[i_couche].append(bot2.neurones[i_couche][i_neurone])
                nbr_bot2 += 1
            else:
                listes_neurones[i_couche].append(bot1.neurones[i_couche][i_neurone])
                nbr_bot1 += 1
            if random() < 1/9:
                listes_neurones[i_couche][i_neurone].mutation() # Attention mutation
    bot3 = Bot(listes_neurones,random()*width,random()*height)
    return bot3


def trie_bot():
    global liste_bots
    for i in range(len(liste_bots)-1):
        if liste_bots[i].rayon < liste_bots[i+1].rayon:
            liste_bots[i], liste_bots[i+1] = liste_bots[i+1], liste_bots[i]
            temp = i
            while temp > 0 and liste_bots[temp].rayon > liste_bots[temp-1].rayon:
                liste_bots[temp], liste_bots[temp-1] = liste_bots[temp -1], liste_bots[temp]
                temp -= 1

def listes_neurones_random(nbr_inputs, nbr_neurones_cache, nbr_output):
    res = [[], []]
    for j in range(nbr_neurones_cache):
        res[0].append(Neurone(liste_poids_random(nbr_inputs)))
    for j in range(nbr_output):
        res[1].append(Neurone(liste_poids_random(nbr_neurones_cache)))
    return res


def liste_poids_random(nbr_input):
    res = []
    for i in range(nbr_input):
        res.append(random())
    return res


def indice_max(liste):
    i_max = 0
    maxi = - float('inf')
    for i in range(len(liste)):
        if liste[i] > maxi:
            i_max = i
            maxi = liste[i]
    return i_max

def start():
    global liste_bots, liste_gems, restart
    for diam in liste_gems:
        diam.effacer()
    liste_gems = []
    if restart:
        for bot in liste_bots:
            bot.effacer()
    liste_bots = []
    for i in range(nbr_gems):
        liste_gems.append(Gem(random() * width, random() * height))
    for i in range(28):
        liste_bots.append(Bot(listes_neurones_random(5, 5, 4), random() * width, random() * height))
    restart = True

# Variable globales
width = 1300
height = 600
liste_bots = []
liste_bots_mort = []
liste_gems = []
nbr_gems = 600
fps = 30
restart = False

# Création de l'interface graphique
root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, background='white')
canvas.pack(side="top")
quit_button = tk.Button(root, text="QUIT", fg="red", command=root.destroy)
quit_button.pack()
generation_button = tk.Button(root, text="Nouvelle Generation", command=nouvelle_generation)
generation_button.pack()


# Main
def main():
    for bot in liste_bots:
        bot.update()
    root.after(1000 // fps, main)

restart_button = tk.Button(root, text="Restart", command=start)
restart_button.pack()

start()
main()
root.mainloop()
