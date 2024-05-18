import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('./机器学习/用户用电数据/RAW_House5_Part2.csv')
#查看基本信息
'''
print(data.head)
print(data.info())
print(data.shape)
print(data.describe())
'''

#和时间有关，向前填充
data = data.ffill()
data = data.bfill()

#data = data.iloc[0:2000]
#拆分时分秒

plt.figure()
x = np.linspace(0,data.shape[0],data.shape[0])
y = data['Aggregate']
plt.plot(x,y)
plt.xlabel('Time')
plt.ylabel('Aggregate')
plt.xticks(x[::100],list(data['Time'][::100]),rotation = 45)
plt.grid(axis = 'y')
plt.show()