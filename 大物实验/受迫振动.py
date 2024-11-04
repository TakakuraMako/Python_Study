import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from sklearn.linear_model import LinearRegression
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 

def table1():
    T_T0 = np.array([1.6296/1.574, 1.5121/1.575, 1.5165/1.575, 1.5301/1.574, 1.5512/1.573, 1.5713/1.570, 1.5912/1.572, 1.6167/1.574, 1.6235/1.574, 1.6278/1.574])
    T0_T = np.array([ 1/x for x in T_T0])
    theta = np.array([62, 49, 53, 65, 99, 131, 104, 74, 67, 63])
    set1 = np.array([])
    set1 = np.column_stack((T_T0, theta))
    set1 = set1[set1[:, 0].argsort()]
    x_smooth = np.linspace(set1[:, 0].min(), set1[:, 0].max(), 300)
    y_smooth = make_interp_spline(set1[:, 0], set1[:, 1], k=3)(x_smooth)
    plt.figure()
    plt.plot(x_smooth, y_smooth)
    plt.scatter(set1[:, 0], set1[:, 1])
    plt.grid()
    plt.xlabel('频率比例' + r'$T_0/T$')
    plt.ylabel('相位差摆轮振幅' + r'$\theta$')
    plt.title('受迫振动的幅频特性曲线')
    plt.show()

def table2():
    T_T0 = np.array([1.6296/1.574, 1.5121/1.575, 1.5165/1.575, 1.5301/1.574, 1.5512/1.573, 1.5713/1.570, 1.5912/1.572, 1.6167/1.574, 1.6235/1.574, 1.6278/1.574])
    T0_T = np.array([ 1/x for x in T_T0])
    phi = np.array([27, 160, 158, 152, 132, 91, 66, 34, 30, 28])
    theta = np.array([62, 49, 53, 65, 99, 131, 104, 74, 67, 63])
    set1 = np.array([])
    set1 = np.column_stack((T_T0, phi))
    set1 = set1[set1[:, 0].argsort()]
    plt.figure()
    plt.plot(set1[:, 0], set1[:, 1])
    plt.grid()
    plt.xlabel('频率比例' + r'$T_0/T$')
    plt.ylabel('相位差' + r'$\phi$')
    plt.title('受迫振动的相频特性曲线')
    plt.show()

table1()
table2()