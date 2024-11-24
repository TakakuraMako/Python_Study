import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
x_1 = np.array([0.0229, 0.0311, 0.0402, 0.0509, 0.0586, 0.0642, 0.0735, 0.0839])
x_2 = np.array([0.0571, 0.0803, 0.1037, 0.1326, 0.1453, 0.1669, 0.1865, 0.2105])
y = list(range( 15, 55, 5))
y = np.array([x*10**-3 for x in y])

model = LinearRegression()
model.fit(x_2.reshape(-1,1),y.reshape(-1,1))
# 生成预测值
y_pred = model.predict(x_2.reshape(-1, 1))
print(model.coef_)
print(model.intercept_)
plt.figure()
plt.scatter(x_2, y)
plt.plot(x_2, y_pred)
plt.xlim(0, max(x_2) + 0.01)
plt.ylim(0, max(y_pred) + 0.005)
plt.grid()
plt.title('无铝盘时m与1/t^2的关系')
plt.xlabel('1/t^2')
plt.ylabel('m')
plt.show()