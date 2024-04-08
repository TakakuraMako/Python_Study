import matplotlib.pyplot as plt
import numpy as np

n = 1024
X = np.random.normal(0, 1, n)#正态分布
Y = np.random.normal(0, 1, n)
T = np.arctan2(Y,X)#颜色
# plt.scatter(X,Y,s=75,c=T,alpha=0.5)
plt.scatter(np.arange(5),np.arange(5))
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
plt.xticks(())#隐藏ticks
plt.yticks(())#隐藏ticks
plt.show()