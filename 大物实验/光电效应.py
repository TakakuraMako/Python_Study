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
    I = np.array([-0.0248, -0.0174, -0.0121, 0.0194, 0.0615, 0.1569,
                0.04, 0.055, 0.086, 0.122, 0.133, 0.188, 0.822, 0.916, 1.080, 1.229, 1.392, 1.574, 1.692, 1.880,
                0.6, 3.82, 7.62, 12.64, 15.85, 18.64,
                21.4, 23.4])
    model = LinearRegression()  # 创建一个回归分析对象
    model.fit(U_Ak.reshape(-1, 1), I.reshape(-1, 1))  # 对x和y进行拟合
    print('系数:', model.coef_[0])
    print('截距:', model.intercept_)
    plt.figure()
    plt.plot(U_Ak, I, '.')
    plt.plot(I, I*model.coef_[0]+model.intercept_)
    plt.grid(True)
    plt.title('伏安特性曲线  ' + r'$\lambda=365mm, \phi=4$')
    plt.ylabel('电压 ' + r'$U_{Ak}/V$')
    plt.xlabel('电流 ' + r'$I/10^{-10}A$')
    plt.show()

def table1():
    f = np.array([8.216, 7.410, 6.882, 5.492, 5.198])
    delta_U = np.array([-1.8016, -1.5124, -1.3356, -0.713, -0.5816])
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

table2()