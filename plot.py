import matplotlib.pyplot as plt

FILE = open("res.data", 'r')

data = FILE.readlines()     # list of lines in FILE
mean = []                   # list of successive means
percent_alive = []
percent_gem_eaten = []

for line in data:
    temp = line.split(" ")

    mean.append(float(temp[0]))
    percent_alive.append(float(temp[1]))
    percent_gem_eaten.append(float(temp[2]))

fig = plt.figure()

ax1 = fig.add_subplot(311)
plt.plot(range(len(mean)), mean)
plt.xlabel("Generation")
plt.ylabel("Mean strength\nof the selected")

ax2 = fig.add_subplot(312)
plt.plot(range(len(percent_alive)), percent_alive)
plt.xlabel("Generation")
plt.ylabel("Percentage of\nremaining alive bots")

ax3 = fig.add_subplot(313)
plt.plot(range(len(percent_gem_eaten)), percent_gem_eaten)
plt.xlabel("Generation")
plt.ylabel("Percentage of\neaten gems in the end")

plt.show()