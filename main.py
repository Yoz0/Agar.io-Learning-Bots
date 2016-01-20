from math import cos, sin, radians
from random import random
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
        return res


class Bot:
    def __init__(self, listes_poids, x, y):
        self.neurones = []
        for i in range(len(listes_poids)):
            temp = []
            for j in range(len(listes_poids[i])):
                temp.append(Neurone(listes_poids[i][j]))
            self.neurones.append(temp)
        self.x = x
        self.y = y
        self.score = 0
        self.rayon = 5
        self.speed = 100
        self.turn_angle = 180
        self.direction = 0  # En degré entre 0 et 360
        self.liste_inputs = [self.x, self.y, 0]  # pos x / pos y / a un diamant
        self.liste_outputs = [0, 0, 0]  # Avancer / droite / gauche
        self.sprite = canvas.create_oval(self.x - self.rayon, self.y - self.rayon,
                                         self.x + self.rayon, self.y + self.rayon, fill='blue')

    def __str__(self):
        return "id : " + str(id(self)) + " position : x = " + str(self.x) + " ; y = " + str(
            self.y) + "\n Neurones : " + str(self.neurones)

    def afficher(self):
        canvas.delete(self.sprite)
        if self.liste_inputs[2] == 1:
            self.sprite = canvas.create_oval(self.x - self.rayon, self.y - self.rayon,
                                             self.x + self.rayon, self.y + self.rayon, fill='red')
        else:
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
        self.liste_inputs[0] = self.x / width
        self.liste_inputs[1] = self.y / height
        if self.liste_inputs[2] == 0:
            if self.detecte_collision_diamant():
                self.liste_inputs[2] = 1
        else:
            if (self.x - (width/2))**2 + (self.y - (height / 2))**2 <= taille_centre**2:
                self.liste_inputs[2] = 0

    def detecte_collision_diamant(self):
        for i in range(len(liste_diamants)):
            diam = liste_diamants[i]
            if (diam.x - self.x) ** 2 + (diam.y - self.y) ** 2 <= self.rayon + diam.rayon:
                self.score += 1
                diam.effacer()
                del liste_diamants[i]
                return True
        else:
            return False

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
        i_max = indice_max(self.liste_outputs)
        if i_max == 0:
            pass
        elif i_max == 1:
            self.direction = (self.direction - self.turn_angle*self.liste_outputs[i_max]/fps) % 360
        elif i_max == 2:
            self.direction = (self.direction + self.turn_angle*self.liste_outputs[i_max]/fps) % 360
        self.x += self.speed * cos(radians(self.direction)) / fps
        self.y += self.speed * sin(radians(self.direction)) / fps


class Diamant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rayon = 3
        self.sprite = canvas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon,
                                         self.y + self.rayon, fill='green')

    def effacer(self):
        canvas.delete(self.sprite)


def listes_poids_random():
    res = [[], []]
    for j in range(4):
        res[0].append(liste_poids_random(3))
    for j in range(3):
        res[1].append(liste_poids_random(4))
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

# Variable globales
width = 900
height = 600
taille_centre = 20
liste_bots = []
liste_diamants = []
fps = 60

# Création de l'interface graphique
root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, background='white')
canvas.pack(side="top")
canvas.create_oval(width//2 - taille_centre, height // 2 - taille_centre,
                   width//2 + taille_centre, height // 2 + taille_centre)
quit_button = tk.Button(root, text="QUIT", fg="red", command=root.destroy)
quit_button.pack()


# Main
def start():
    global liste_bots, liste_diamants
    for diam in liste_diamants:
        diam.effacer()
    liste_diamants = []
    for bot in liste_bots:
        bot.effacer()
    liste_bots = []
    for i in range(40):
        liste_diamants.append(Diamant(random() * width, random() * height))
    for i in range(15):
        liste_bots.append(Bot(listes_poids_random(), width // 2, height // 2))

restart_button = tk.Button(root, text="Restart", command=start)
restart_button.pack()


def main():
    for bot in liste_bots:
        bot.update()
    root.after(1000//fps, main)

start()
main()
root.mainloop()
