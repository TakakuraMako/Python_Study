import matplotlib.pyplot as plt
import numpy as np

n = 12
X = np.arange(n)
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
plt.bar(X, Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2,)

for x,y in zip(X, Y1):
    plt.text(x+0.4)

plt.xlim((-1,12))
plt.xticks(())
plt.yticks(())

plt.show()