import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import math
from sklearn.linear_model import LinearRegression
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
T = np.array([1.5167, 1.5312, 1.5506, 1.5721, 1.5928, 1.6170, 1.6243, 1.6278, 1.63, 1.6326])
T0 = np.array([1.582, 1.582, 1.579, 1.573, 1.576, 1.580, 1.580, 1.581, 1.581, 1.581])
T0_T = np.array([1.582/1.5167, 1.582/1.5312, 1.579/1.5506, 1.573/1.5721, 1.576/1.5928, 1.580/1.6170, 1.580/1.6243, 1.581/1.6278, 1.581/1.63, 1.581/1.6326])
# print(T0_T)
def table1():
    theta1 = np.array([163, 150, 137, 126, 116, 106, 97, 89, 82, 75])
    theta2 = np.array([142, 128, 115, 103, 93, 84, 75, 67, 60, 53])
    theta3 = np.array([160, 144, 130, 118, 106, 96, 86, 78, 70, 63])
    theta = np.stack((theta1, theta2, theta3))
    T = np.array([1.5752, 1.5791, 1.5758])
    beta = np.array([])
    for n in range(3):
        b = 0
        for i in range(5):
            b += math.log(theta[n][i]/theta[n][i+5])
        print(round(b/5, 3))
        beta.append(round(b/5/T[n], 3))



def table2(T0_T):
    theta = np.array([44, 59, 88, 130, 112, 80, 72, 69, 67, 65])
    set1 = np.array([])
    set1 = np.column_stack((T0_T, theta))
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

def table3(T0_T, T, T0):
    phi = np.array([157, 154, 139, 96, 59, 38, 33, 31, 30, 29])
    phi = -phi
    phi_theory = []
    beta = 0.327
    rate_2 = []
    for i in range(10):
        phi_theory.append(round(math.degrees(math.atan(-beta * 2 * 2*math.pi/T[i]/((math.pi * 2 / T0[i])**2 - (math.pi * 2 / T[i])**2))), 2))
        rate_2.append(round(beta**2 / ((2*math.pi/T[i] - 2*math.pi/T0[i])**2 + beta**2), 3))
    rate = np.array([math.sqrt(x) for x in rate_2])
    print(rate, rate_2, phi_theory, sep='\n')
    plt.figure()
    plt.plot(T0_T, phi)
    plt.grid()
    plt.xlabel('频率比例' + r'$T_0/T$')
    plt.ylabel('相位差' + r'$\phi$')
    plt.title('受迫振动的相频特性曲线')
    plt.show()

table3(T0_T, T, T0)