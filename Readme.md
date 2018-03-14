Agar.io Learning Bots
=====================
This is a python project to test a combination of neural network and genetic
algorithm in order to create a good artificial intelligence.
The bots have to collect gems and eat each other like in the game <agar.io>, but
we changed some rules to facilitate the neural network approach. The bots move
on a grid, they can eat gems to get stronger, they can also eat weaker bots to
get even stronger.

Neural Network
--------------
Each bot has a
[neural network](https://en.wikipedia.org/wiki/Artificial_neural_network) made
of layers of neurons.

### First Version
* one layer of 4 Neurons.

#### Inputs
* Gem up (1 if there is, 0  if there isn't )
* Gem down
* Gem left
* Gem right
* Foe up (1 if there is a weaker foe, 0 if there isn't, -1 if there is a
stronger foe)
* Foe down
* Foe left
* Foe right

#### Outputs
* Go up
* Go down
* Go left
* Go right

### Second Version
* first layer : NBR_BOT+NBR_GEMS neurons
* second layer : 4 neurons

#### Inputs
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
When the user hits the "New Generation" button, the program searches for the
NB_SELECT_BOT strongest bots (dead or alive) and creates NBR_BOT new ones with
[crossover](https://en.wikipedia.org/wiki/Crossover_%28genetic_algorithm%29)
and [mutation](https://en.wikipedia.org/wiki/Mutation_%28genetic_algorithm%29).

Technical stuff
---------------
We use python 3.5 and Tkinter. Use `./main.py` to run, `./plot.py` to have a
recap of the run you just made.

### Dependancies :
* tkinter (for the UI) : `sudo apt-get install python3-tk`
* matplotlib (for plot.py) : `sudo apt-get install python3-matplotlib`


State of the project
--------------------
Edit made the 2018-03-13

Two years after I can now see that we have made a lot of mistakes:
Backpropagation would have been put to a good use here. The project was a mess,
a better organisation in the code would have really helped us. It got a lot
better when Clément came in, but it would have been better to start on good
basis from the beginning. Also the implementation of the neurons is lacking a
random input (I tried a bit of this in another branch `AddRandom` some time
after the project was already finished).

Yet this project is now considered finish and we are satisfied of the project as
it is. You can see a demonstration of the project in
[this video](https://www.youtube.com/watch?v=DG2iipxHxe0), in French.

Developers
----------
This is a personal project by Clément Saintier and Stéphane Kastenbaum.
