import unittest
from main import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_Neuron(self):
        ner = Neuron(3)
        ner.list_weight = [0, 0, 0]
        self.assertEqual(ner.output([0, 0, 0]), 0.5)
        ner = Neuron(1)
        ner.list_weight = [1]
        self.assertEqual(ner.output([-1]), 1/(exp(1)+1))
        # Test the case when list_input.len() != list_weight.len()
        self.assertEqual(ner.output([1, 1]), None)

    def test_Bot(self):
        global list_bot
        b1 = Bot([[Neuron(1)], [Neuron(1)]], 1, 1)
        b2 = Bot([[Neuron(1)], [Neuron(1)]], 1, 2)
        list_bot = [b1, b2]
        self.assertEqual(b1.detect_foe(1, 2), b2)
        self.assertEqual(b1.detect_foe(1, 1), None)




if __name__ == '__main__':
    unittest.main()
