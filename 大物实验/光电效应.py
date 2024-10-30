import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
def table2():
    U_Ak = np.arange(-2.0, 0.0, 0.1)
    U_Ak = np.append(U_Ak, np.arange(0.0, 18.0, 3))
    U_Ak = np.append(U_Ak, np.array([18.0, 20.0]))
    I = np.array([-0.36, -0.34, -0.33, -0.3, -0.27, -0.2, -0.1, 0.01, 0.17, 0.33, 0.43, 0.68, 0.85, 1.0, 1.27, 1.51, 1.72, 2.05, 2.24, 2.56, 3.2, 14.1, 27.3, 35.8, 43.8, 50.2, 56.2, 59.7])
    model = LinearRegression()  # 创建一个回归分析对象
    model.fit(I.reshape(-1, 1), U_Ak.reshape(-1, 1))  # 对x和y进行拟合
    print('系数:', model.coef_[0])
    print('截距:', model.intercept_)
    plt.figure()
    plt.plot(I, U_Ak, 'o')
    plt.plot(I, I*model.coef_[0]+model.intercept_)
    plt.grid(True)
    plt.title('伏安特性曲线  ' + r'$\lambda=365mm, \phi=4$')
    plt.ylabel('电压 ' + r'$U_{Ak}/V$')
    plt.xlabel('电流 ' + r'$I/10^{-12}A$')
    plt.show()

def table1():
    f = np.array([8.216, 7.410, 6.882, 5.492, 5.198])
    delta_U = np.array([-1.428, -0.994, -0.858, -0.514, -0.436])
    model = LinearRegression()  # 创建一个回归分析对象
    model.fit(f.reshape(-1, 1), delta_U.reshape(-1, 1))  # 对x和y进行拟合
    print('系数:', model.coef_[0])
    print('截距:', model.intercept_)
    plt.figure()
    plt.plot(f, delta_U, '.')
    plt.plot(f, f*model.coef_[0] + model.intercept_, '-')
    plt.title('截止电压'+r'$U$'+'与光的频率'+r'$v$'+'的关系')
    plt.xlabel(r'$v/10^{14}Hz$')
    plt.ylabel(r'$U/V$')
    plt.show()

table1()