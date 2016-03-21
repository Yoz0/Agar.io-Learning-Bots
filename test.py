import unittest
from main import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_Neuron(self):
        ner = Neuron([0, 0, 0])
        self.assertEqual(ner.output([0, 0, 0]), 0.5)
        ner = Neuron([1])
        self.assertEqual(ner.output([-1]), 1/(exp(1)+1))
        # Test the case when list_input.len() != list_weight.len()
        with self.assertRaises(ValueError):
            ner.output([0,0])

    def test_Gem(self):
        g1 = Gem(0, 0)
        list_gem = [g1]
        self.assertEqual(g1.detect_gem(0, 0, list_gem), g1)
        self.assertEqual(g1.detect_gem(0, 1, list_gem), None)

    def test_Bot(self):
        b1 = Bot(8, Neural_network([4], 8),0,0)
        b2 = Bot(8, Neural_network([4], 8), 0, 1)  # b2 is just below b1
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
        b1.list_output = [0,1,0,0]
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


    def test_selection(self):
        list_bot = []
        for i in range(MAX_STRENGTH):
            list_bot.append(Bot(8, Neural_network([4], 8),0,0))
            list_bot[i].strength = randrange(MAX_STRENGTH)
        best = selection(list_bot, 10)
        for i in range(len(best)-1):
            self.assertGreaterEqual(best[i].strength, best[i+1].strength)

    def test_crossover(self):
        lb1 = []
        lb2 = []
        for i_layer in range(1):
            ll1 = []
            ll2 = []
            for i_neuron in range(4):
                ll1.append(Neuron([0,0,0,0]))
                ll2.append(Neuron([1,1,1,1]))
            lb1.append(Layer(ll1))
            lb2.append(Layer(ll2))
        b1 = Neural_network(lb1)
        b2 = Neural_network(lb2)
        bot1 = Bot(1, b1, 0, 0)
        bot2 = Bot(1, b2, 0, 0)
        bot3 = crossover(bot1, bot2)
        for layer in bot3.brain:
            nbr_from_bot1 = 0
            for neuron in layer:
                if neuron.list_weight[0] == 1:
                    nbr_from_bot1 += 1
            self.assertEqual(nbr_from_bot1, len(layer)//2)


if __name__ == '__main__':
    unittest.main()
