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

    def test_Gem(self):
        g1 = Gem(0, 0)
        list_gem = [g1]
        self.assertEqual(g1.detect_gem(0, 0, list_gem), g1)
        self.assertEqual(g1.detect_gem(0, 1, list_gem), None)

    def test_Bot(self):
        b1 = Bot(list_neuron_random(8, 8, 4), 0, 0)
        b2 = Bot(list_neuron_random(8, 8, 4), 0, 1)  # b2 is just below b1
        list_bot = [b1, b2]
        list_dead_bot = []
        g1 = Gem(0, 0)
        g2 = Gem(1, 0)  # g2 is right to b1
        list_gem = [g1, g2]
        self.assertEqual(b1.detect_foe(0, 1, list_bot), b2)
        self.assertEqual(b1.detect_foe(0, 0, list_bot), None)
        self.assertEqual(b1.detect_foe(0, 2, list_bot), None)
        b1.update_input(list_bot, list_gem)
        for i in range(8):
            if i == 5:
                self.assertEqual(b1.list_input[i], -1)
            elif i == 3:
                self.assertEqual(b1.list_input[i], 1)
            else:
                self.assertEqual(b1.list_input[i], 0)
        b1.update_output()
        for i in range(4):
            self.assertGreaterEqual(b1.list_output[i], 0)
            self.assertLessEqual(b1.list_output[i], 1)
        print(b1.list_output)
        b1.eat(list_bot, list_gem, [])
        self.assertListEqual(list_gem, [g2])
        self.assertEqual(b1.strength, 1)
        b1.move()
        self.assertEqual(b1.i, 0)
        self.assertEqual(b1.j, 1)
        b1.eat(list_bot,list_gem,list_dead_bot)
        self.assertEqual(b1.strength, 6)
        self.assertListEqual(list_bot, [b1])
        self.assertListEqual(list_dead_bot,[b2])







if __name__ == '__main__':
    unittest.main()
