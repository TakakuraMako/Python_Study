import numpy as np
import matplotlib.pyplot as plt

# 定义微分方程 dy/dx = f(x, y)
def f(x, y):
    return x - y  

# 创建网格
x_values = np.linspace(-5, 5, 20)
y_values = np.linspace(-5, 5, 20)
X, Y = np.meshgrid(x_values, y_values)

# 计算矢量分量
U = 1  # x方向的分量
V = f(X, Y)  # y方向的分量

# 绘制方向场
plt.quiver(X, Y, U, V)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Direction Field of dy/dx = f(x, y)')
plt.grid(True)
plt.show()
