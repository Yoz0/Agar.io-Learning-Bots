Agar.io Learning Bots
=====================
This is a python project to test a combination of neural network and genetic algorithm in order to create Awe.
The bots have to collect gems and eat each other like in the game <agar.io>, but we changed some rules to facilitate the neural network approach. The bots move on a grid, they can eat gems to get stronger, they can also eat weaker bots to get even stronger.

Neural Network
--------------
Each bot has a [neural network](https://en.wikipedia.org/wiki/Artificial_neural_network) made of layers of neurons.
###First Version
* one layer of 4 Neurons.

####Inputs
* Gem up (1 if there is, 0  if there isn't )
* Gem down
* Gem left
* Gem right
* Foe up (1 if there is a weaker foe, 0 if there isn't, -1 if there is a stronger foe)
* Foe down
* Foe left
* Foe right

####Outputs
* Go up
* Go down
* Go left
* Go right

###Second Version
* first layer : NBR_BOT+NBR_GEMS neurons
* second layer : 4 neurons

####Inputs
For each other bot
* The difference (hisY - myY)
* The difference (hisX - myX)
* The distance between the bot and I (+ if I'm stronger, - if I'm weaker)

For each gem
* The difference (hisY - myY)
* The difference (hisX - myX)
* The distance between the gem and I

Genetic Algorithm
-----------------
When the user hits the "New Generation" button, the program searches for the NB_SELECT_BOT strongest bots (dead or alive) and creates NBR_BOT new ones with
[crossover](https://en.wikipedia.org/wiki/Crossover_%28genetic_algorithm%29) 
and [mutation](https://en.wikipedia.org/wiki/Mutation_%28genetic_algorithm%29).

Technical stuff
---------------
We use python 3.5 and Tkinter. Use `python3 main.py` to run, `python3 plot.py` to have a recap of the run you just made.

Dependancies :
* tkinter (for the UI) : `sudo apt-get install python3-tk` if you're on linux
* matplotlib (for plot.py) : `sudo apt-get install python3-matplotlib` if you're on linux

Developers
----------
This is a personal project by Clément Saintier and Stéphane Kastenbaum.
