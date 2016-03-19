from gem import *
from useful import *
from config import *

class Bot:
    """
    This is a bot.
    """
    def __init__(self, list_neuron, i, j):
        self.list_neuron = list_neuron
        self.i = i
        self.j = j
        self.strength = 0
        self.list_input = [0 for i in range(8)]
        self.list_output = [0, 0, 0, 0]  # up / down / left / right
        self.sprite = None

    def __str__(self):
        return "id : " + str(id(self)) + " position : i = " + str(self.i) + " ; j = " + str(
            self.j) + "Strength : " + str(self.strength) + "\n Neurons : " + str(self.list_neuron)

    def display(self):
        """
        Display the bot at the position i;j on the canvas.
        Canvas should be a global ariable.
        """
        canvas.delete(self.sprite)
        self.sprite = canvas.create_oval(self.i * SQUARE_SIZE, self.j * SQUARE_SIZE,
                                         (self.i + 1) * SQUARE_SIZE, (self.j+1) * SQUARE_SIZE,
                                         fill=int_to_color(self.strength))

    def erase(self):
        """
        Erase the sprite from canvas
        """
        canvas.delete(self.sprite)

    def update(self, list_bot, list_gem):
        """
        Compute the input
        Calculate the output
        Move according to the output
        and update the display
        """
        self.update_input(list_bot, list_gem)
        self.update_output()
        self.move()
        self.display()

    def update_input(self, list_bot, list_gem):
        """
        Check up, down, left and right to see if there is any foe or gem and update self.list_input accordingly
        """
        self.list_input = [0 for k in range(8)]
        if Gem.detect_gem(self.i, self.j - 1, list_gem) is not None:
            self.list_input[0] = 1
        if Gem.detect_gem(self.i, self.j + 1, list_gem) is not None:
            self.list_input[1] = 1
        if Gem.detect_gem(self.i - 1, self.j, list_gem) is not None:
            self.list_input[2] = 1
        if Gem.detect_gem(self.i + 1, self.j, list_gem) is not None:
            self.list_input[3] = 1
        foe = self.detect_foe(self.i, self.j - 1, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[4] = 1
            else:
                self.list_input[4] = -1
        foe = self.detect_foe(self.i, self.j + 1, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[5] = 1
            else:
                self.list_input[5] = -1
        foe = self.detect_foe(self.i - 1, self.j, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[6] = 1
            else:
                self.list_input[6] = -1
        foe = self.detect_foe(self.i + 1, self.j, list_bot)
        if foe is not None:
            if foe.strength < self.strength:
                self.list_input[7] = 1
            else:
                self.list_input[7] = -1

    def detect_foe(self, i, j, list_bot):
        """
        Detect if there is a foe (a bot different than me) at the location i, j
        :param i: the line
        :param j: the column
        :return: the foe if there is one, None if not.
        """
        k = 0
        while k < len(list_bot):
            foe = list_bot[k]
            if foe.i == i and foe.j == j and self != foe:
                return foe
            k += 1
        return None

    def update_output(self):
        """
        Calculate each output of the neurons and
        set list_output as the proper value.
        """
        temp_inputs = self.list_input[:]  # Copy the list
        temp_outputs = []
        for layer in self.list_neuron:
            # for each layer of neurons
            for neuron in layer:
                # for each neuron in this layer
                temp_outputs.append(neuron.output(temp_inputs))
                # we add to temp_outputs the output of the neuron self.list_neuron[i_layer][i_neuron]
                # with temp_inputs as inputs
            temp_inputs = temp_outputs[:]
            temp_outputs = []
        self.list_output = temp_inputs[:]

    def move(self):
        """
        Check which out put is the "most activated" (which is higher) and move in that direction
        :return:
        """
        i_max = max_index(self.list_output)
        if i_max == 0 and self.j > 0:
            self.j -= 1
        elif i_max == 1 and self.j < HEIGHT-1:
            self.j += 1
        elif i_max == 2 and self.i > 0:
            self.i -= 1
        elif i_max == 3 and self.i < WIDTH-1:
            self.i += 1

    def eat(self, list_bot, list_gem, list_dead_bot):
        """
        Check if there is a weaker foe or a Gem at my location, if so, eat it!
        """
        gem = Gem.detect_gem(self.i, self.j, list_gem)
        if gem is not None:
            if self.strength < MAX_STRENGTH:
                self.strength += 1
            gem.erase()
            list_gem.remove(gem)
        foe = self.detect_foe(self.i, self.j, list_bot)
        if foe is not None:
            if self.strength+5 <= MAX_STRENGTH:
                self.strength += 5
            foe.erase()
            list_dead_bot.append(foe)
            list_bot.remove(foe)
