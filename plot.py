import numpy as np
import matplotlib.pyplot as plt

FILE = open("res.data", 'r')

data = FILE.readlines()
for i in range(len(data)):
    data[i] = float(data[i])

plt.plot(range(len(data)), data)
plt.xlabel("Generation")
plt.ylabel("Mean strength of the selected")
plt.show()