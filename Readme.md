Agar.io Learning Bots
=====================
This is a python project to test combination of neural network and genetic algorithm in order to do create AI.
The bots have to collect gems and eat each other like in the game <agar.io>,
but I changed some rules to facilitate the neural network approach. The bots move on a grid, they can eat gems to become
 stronger, they can eat other weaker bot to become even more stronger.

Neural Network
--------------
Each bots has a two layer [neural network](https://en.wikipedia.org/wiki/Artificial_neural_network).
Fist layer has 8 neurons, second layer has 4.
###Inputs
* Gem up (1 if there is, 0  if there isn't )
* Gem down
* Gem left
* Gem right
* Foe up (1 if there is a weaker foe, 0 if there isn't, -1 if there is a stronger foe)
* Foe down
* Foe left
* Foe right

###Outputs
* Go up
* Go down
* Go left
* Go right

Genetic Algorithm
-----------------
When the user hit the "New Generation" button, the program search for the 7 stronger bots (dead or alive) and create 21 new ones with
[crossover](https://en.wikipedia.org/wiki/Crossover_%28genetic_algorithm%29) 
and [mutation](https://en.wikipedia.org/wiki/Mutation_%28genetic_algorithm%29).

Technical stuff
_______________
I use python 3.5 and Tkinter
