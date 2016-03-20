from copy import *
from layer import *

class Neural_network:
	"""This class represents a neural network that can have several layers.
	A neural network takes a given number of inputs and yields the same number
	of outputs as the number of neurons in the last layer"""

	def __init__(self, arg1, arg2 = None):
		"""
		method 1 : my_net = neural_network(list_sizes, nbr_input)
			inits a neural network that has 'len(list_sizes)' layers, their respective
			size (number of neurons in the given layer) should be given by list_sizes,
			where list_sizes[n] is the size of the nth layer
		method 2: my_net = neural_network(list_layers)
			inits a neural network that has list_layers for layers. This function
			also check the validity of such a network (it checks if every layer takes
			as much input as there is neurons in the previous layer)
		"""

		if  isinstance(arg1, list) and isinstance(arg2, int):
			#method 1
			list_sizes = arg1
			nbr_input = arg2

			self.layers = []
			self.nbr_layer = len(list_sizes)
			self.nbr_input = nbr_input

			cur_nbr_input = nbr_input   #needed to make every layer take the same number
										#of input that the previous layer had neurons
			for i in range(self.nbr_layer):
				self.layers.append(Layer(list_sizes[i], cur_nbr_input))
				cur_nbr_input = list_sizes[i]
		elif isinstance(arg1, list) and arg2 == None:
			#check if arg1 is a list of layers
			for a in arg1:
				if not isinstance(a, Layer):
					raise TypeError("In 'Neural_network.__init__()' : The list you provided does not only contain Layers. It should.")

			#method 2
			self.layers = deepcopy(arg1)
			self.nbr_layer = len(self.layers)
			self.nbr_input = self.layers[0].nbr_input

			cur_nbr_input = self.nbr_input
			for layer in self.layers:
				if layer.nbr_input != cur_nbr_input:
					raise ValueError("In 'Neural_network.__init__() : the layers provided do not form a valid network\n")
				cur_nbr_input = layer.nbr_neuron
		else:
			raise TypeError("In 'Neural_network.__init__()': wrong arguments.\n")

	def get_output(self, inputs):
		"""
		Feeds the first layer of the net with 'inputs', and then feeds every output
		from one layer to the following. returns the output from the last layer 
		"""

		#protection
		if len(inputs) != self.nbr_input:
			raise TypeError("In 'Neural_network.get_output()': wrong number of input. Given " + str(len(inputs)) + " needed " + str(len(self.nbr_input)) + ".\n")

		cur_input = []		#will hold the successive result of each layer
		cur_input = inputs

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

	#The following functions were created in order to meet python's protocol for
	#sequences. (protocol = interface in python)
	#with the following function, 'Neural_network' will act as a "sequence"
	#(like a list) of layers. eg: 'for layer in neural_network:'
	def __len__(self):
		return self.nbr_layer

	def __getitem__(self, key):
		if(key >= self.nbr_layer):
			raise ValueError("in 'Layer.__getitem__()' : No such layer. There is only " + str(nbr_layer) + ", you asked for 'neural_network[" + str(key) + "]'.\n")
		return self.layer[key]

	def __setitem__(self, key, value):
		if(key >= self.nbr_layer):
			raise valueError("in 'Layer.__setitem__()' : No such layer. There is only " + str(nbr_layer) + ", you asked for 'neural_network[" + str(key) + "]'.\n")

		if not isinstance(value, Layer):
			raise TypeError("in 'Layer.__setitem__()' : neural_network only contains layers, not " + str(type(value)) + "s.\n")

		self.layers[key] = value

	def __delitem__(self, key):
		return self.layers.__delitem__(key)

	def __iter__(self):
		return self.layers.__iter__()

	def __reversed__(self):
		return self.layers.__reversed__()