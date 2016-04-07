from copy import *
from layer import *


class NeuralNetwork:
    """This class represents a neural network that can have several layers.
    A neural network takes a given number of inputs and yields the same number
    of outputs as the number of neurons in the last layer"""

    def __init__(self, list_layers):
        """
        usage : my_net = neural_network(list_layers)
        Inits a neural network that has list_layers for layers. This function
        also check the validity of such a network (it checks if every layer takes
        as much input as there is neurons in the previous layer).
        :param list_layers: List of layers from which to create the neural network.
                            This list is deepcopy'ed.
        """
        # check if list_layers is a list of layers
        for a in list_layers:
            if not isinstance(a, Layer):
                raise TypeError("In 'NeuralNetwork.__init__()' :"
                                " The list you provided does not only contain Layers. It should.")

        # check validity of layers
        cur_nbr_input = list_layers[0].nbr_input
        for layer in list_layers:
            if layer.nbr_input != cur_nbr_input:
                raise ValueError("In 'NeuralNetwork.__init__() : the layers provided do not form a valid network\n")
            cur_nbr_input = layer.nbr_neuron

        # actual function
        self.layers = deepcopy(list_layers)
        self.nbr_layer = len(self.layers)
        self.nbr_input = list_layers[0].nbr_input
        self.nbr_output = len(list_layers[-1])  # list[-1] -> last element of list

    @staticmethod
    def quick_init(list_sizes, nbr_input):
        """
        Usage : my_net = NeuralNetwork.random_init(list_sizes, nbr_input)
        Inits a neural network that has 'len(list_sizes)' layers, their respective
        size (number of neurons in the given layer) should be given by list_sizes,
        where list_sizes[n] is the size of the nth layer
        :return: a bot created as described.
        """
        if not isinstance(list_sizes, list):
            raise TypeError("In 'NeuralNetwork.init_random' : argument 'list_sizes' has to be a list.")
        for a in list_sizes:
            if not isinstance(a, int):
                raise TypeError("In 'NeuralNetwork.init_random' : list_sizes should only contain integers.")
        if not isinstance(nbr_input, int):
            raise TypeError("In 'NeuralNetwork.init_random' : argument 'nbr_input' should be an integer")

        list_layers = []
        cur_nbr_input = nbr_input  # needed to make every layer take the same number
        # of input that the previous layer had neurons
        for i in range(len(list_sizes)):
            list_layers.append(Layer.random_init(list_sizes[i], cur_nbr_input))
            cur_nbr_input = list_sizes[i]
        return NeuralNetwork(list_layers)

    def get_output(self, inputs):
        """
        Feeds the first layer of the net with 'inputs', and then feeds every output
        from one layer to the following. returns the output from the last layer
        """
        if not isinstance(inputs, list):
            raise TypeError("In 'NeuralNetwork.get_output()' : argument 'inputs' has to be a list.")

        if len(inputs) != self.nbr_input:
            raise TypeError(
                "In 'NeuralNetwork.get_output()': wrong number of input. Given " + str(len(inputs)) + " needed " + str(
                    self.nbr_input) + ".\n")

        cur_input = inputs  # will hold the successive result of each layer
        for layer in self.layers:
            cur_input = layer.get_output(cur_input)
        return cur_input

    def __repr__(self):
        res = ""
        res += "This neural network takes " + str(self.nbr_input) + " inputs.\n"
        for i, layer in enumerate(self.layers):
            res += "Layer " + str(i) + " :\n"
            res += str(layer)
        return res

    def same_structure(self, brain2):
        """
        Returns 1 if brain2 has the same structure as self
        Same structure implies same number of inputs, same number of layers,
        same number of neurons on each layers
        """
        if not isinstance(brain2, NeuralNetwork):
            raise TypeError("In 'neural_network.crossover()': neural_network expected, " + str(type(brain2)) + " given.")
        if self.nbr_input != brain2.nbr_input:
            return 0
        if len(self.layers) != len(brain2.layers):
            return 0

        for i in range(len(self.layers)):
            if len(self.layers[i]) != len(brain2.layers[i]):
                return 0

        return 1

    def crossover(self, brain2):
        """Creates a new neural_network, crossover from self and brain2. The new
        network brain takes exactly (and for each layer) half his neurons from 'self'
        and the other half from 'brain2' : only the distribution on each layer
        is random.
        :return: a new bot with, on each layer, as many neurons from bot 1 as bot 2.
        """
        # protection
        if not isinstance(brain2, NeuralNetwork):
            raise TypeError("In 'neural_network.crossover()': neural_network expected, " + str(type(brain2)) + " given.")
        if not self.same_structure(brain2):
            raise ValueError("In 'neural_network.crossover()':"
                             " the neural_network provided doesn't have the same structure as 'self'")

        list_layer_brain3 = []         # layers of the neural net of brain3

        for i_layer, layer in enumerate(self.layers):
            list_neurons = []   # neurons that we will insert in brain3 as a layer
            nbr_neuron_from_self = len(layer)//2

            # We have to select nbr_neuron_from_self integers in the sequence range(len(layer))
            index_of_neurons_from_self = []
            for i in range(nbr_neuron_from_self):
                index = randrange(len(layer))
                while index in index_of_neurons_from_self:    # We don't want the same index twice
                    index = randrange(len(layer))
                index_of_neurons_from_self.append(index)

            for i in range(len(layer)):
                if i in index_of_neurons_from_self:
                    list_neurons.append(deepcopy(self[i_layer][i]))
                else:
                    list_neurons.append(deepcopy(brain2[i_layer][i]))

            list_layer_brain3.append(Layer(list_neurons))

        return NeuralNetwork(list_layer_brain3)

    def mutation(self, avg):
        """
        Mutate (or not) the neural network
        :param avg: the avergae of brain who will be mutated if you call this function with a tons of neural network
        :return:
        """
        for l in self.layers:
            l.mutation(avg / len(self.layers))

    # The following functions were created in order to meet python's protocol for
    # sequences. (protocol = interface in python)
    # with the following function, 'NeuralNetwork' will act as a "sequence"
    # (like a list) of layers. eg: 'for layer in neural_network:'
    def __len__(self):
        return self.nbr_layer

    def __getitem__(self, key):
        if key >= self.nbr_layer:
            raise ValueError("in 'Layer.__getitem__()' : No such layer. There is only " + str(self.nbr_layer) + ", you asked for 'neural_network[" + str(key) + "]'.\n")
        return self.layers[key]

    def __setitem__(self, key, value):
        if key >= self.nbr_layer:
            raise ValueError("in 'Layer.__setitem__()' : No such layer. There is only " + str(self.nbr_layer) + ", you asked for 'neural_network[" + str(key) + "]'.\n")

        if not isinstance(value, Layer):
            raise TypeError("in 'Layer.__setitem__()' : neural_network only contains layers, not " + str(type(value)) + "s.\n")

        self.layers[key] = value

    def __delitem__(self, key):
        return self.layers.__delitem__(key)

    def __iter__(self):
        return self.layers.__iter__()

    def __reversed__(self):
        return self.layers.__reversed__()
