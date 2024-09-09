import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
def table_1():
    theta = range(-90, 100, 10)
    U_m = [0.5, 0.6, 2.3, 3.8, 5.2, 6.3, 7.4, 8.2, 8.7, 9.3, 9.3, 9.1, 8.6, 7.9, 6.7, 5.4, 4.1, 2.5, 0.9]
    epsilon = [round(math.sqrt(2) * x, 2) for x in U_m]
    print(epsilon)
    plt.figure()
    plt.plot(theta, U_m, marker = 'o')
    plt.xticks(theta)
    plt.yticks(np.arange(0.0, max(U_m)+1))
    plt.xlabel('探测线圈转角' + r'$ \theta/° $')
    plt.ylabel(r'$ \epsilon_{max} $')
    plt.title('探测线圈法线与磁场方向不同夹角数据记录')
    for xi, yi in zip(theta, U_m):
        plt.text(xi-5, yi+0.3, yi)
    plt.grid()
    plt.show()

def table_2():
    x = np.arange(-0.1, 0.11, 0.01)
    x_1 = np.arange(-10, 11, 1)
    print(x)
    U_m = (4.4, 5.1, 5.9, 6.9, 7.8, 8.9, 10.0, 11.1, 11.9, 12.4, 12.7, 12.4, 11.9, 11.1, 10.1, 9.1, 8.0, 6.9, 6.0, 5.2, 4.5)
    B_m = [round(0.103 * x, 2) for x in U_m]
    mu_0 = 4 * math.pi * math.pow(10, -7)
    N_0 = 400.0
    I = 0.4
    R = 0.1
    B_lilun = [round(mu_0 * N_0 * I * R**2 / 2 / math.pow(R**2 + y**2, 1.5) * 1000, 2) for y in x]
    print(f'B_m:{B_m}')
    print(f'B_lilun:{B_lilun}')
    plt.figure()
    plt.plot(x_1, B_m, marker = 'o')
    plt.plot(x_1, B_lilun, marker = '*')
    plt.xticks(np.arange(-10, 11, 2))
    plt.xlabel('轴向距离' + r'$ x/cm $')
    plt.ylabel(r'$ B / mT $')
    plt.title('圆电流线圈轴上磁场分布的数据')
    plt.grid()
    plt.show()


def table_3():
    x = np.arange(-5.0, 6.0, 1)
    U_m = [15.5, 14.6, 13.6, 13.1, 12.7, 12.6, 12.6, 12.9, 13.4, 14.1, 15.4]
    B_m = [round(x * 0.103, 3) for x in U_m]
    print(f'B_m:{B_m}')
    plt.figure()
    plt.plot(x, B_m, marker = 'o')
    plt.xticks(x)
    plt.xlabel('径向距离' + r'$ x/cm $')
    plt.ylabel(r'$ B_m/mT $')
    plt.title('测量圆电流线圈沿径向的磁场分布')
    for xi, yi in zip(x, B_m):
        plt.text(xi, yi+0.01, yi)
    plt.grid()
    plt.show()

def table_4():
    x = np.arange(-10, 11, 1)
    U_m = [10.8, 12.4, 14.5, 16.7, 18.5, 19.3, 19.5, 19.0, 18.3, 17.7, 17.4, 17.5, 18.0, 18.7, 19.2, 19.3, 18.3, 16.6, 15.1, 12.9, 11.5]
    B_m = [round(x * 0.103, 2) for x in U_m]
    print(f'B_m:{B_m}')
    plt.figure()
    plt.plot(x, B_m, marker = 'o')
    plt.xticks(x)
    plt.xlabel('轴向距离' + r'$ x/cm $')
    plt.yticks(np.arange(0, max(B_m)))
    plt.ylabel(r'$ B_m/mT $')
    plt.title('亥姆霍兹圈轴线上的磁场分布')
    for xi, yi in zip(x, B_m):
        plt.text(xi, yi+0.01, yi)
    plt.grid()
    plt.show()

def table_5():
    f = range(50, 160, 10)
    U_m = [18.0, 19.2, 20.1, 20.7, 21.0, 21.5, 21.8, 22.0, 22.2, 22.3, 22.4]
    B_m = []
    for i in range(len(f)):
        B_m.append(round(5.171 * U_m[i] / f[i], 2))
    print(f'B_m{B_m}')
    plt.figure()
    plt.plot(f, B_m, marker = 'o')
    plt.xticks(f)
    plt.xlabel('励磁电流频率' + r'$ f/Hz $')
    plt.yticks(np.arange(0, math.ceil(max(B_m))+1))
    plt.ylabel(r'$ B_m/mT $')
    plt.title('励磁电流频率变化对磁场的影响')
    for xi, yi in zip(f, B_m):
        plt.text(xi, yi+0.01, yi)
    plt.grid()
    plt.show()

def table_6():
    x = range(-10, 11, 1)
    U_2R = [14.1, 13.8, 13.5, 12.9, 12.2, 11.4, 10.6, 10.0, 9.4, 9.1, 8.9, 9.0, 9.3, 9.8, 10.4, 11.1, 12.0, 12.7, 13.5, 13.8, 14.0]
    U_halfR = [9.4, 10.6, 12.3, 14.1, 15.9, 17.8, 19.4, 21.0, 22.1, 23.0, 23.3, 23.0, 21.8, 21.1, 19.9, 18.2, 16.4, 14.4, 12.7, 11.0, 9.8]
    B_2R = [round(0.103 * x , 2) for x in U_2R]
    B_halfR = [round(0.103 * x , 2) for x in U_halfR]
    print(f'B_2R:{B_2R}\nB_halfR:{B_halfR}')
    plt.figure()
    plt.plot(x, B_2R, marker = 'o', label = r'$d=2r$')
    plt.plot(x, B_halfR, marker = '*', label = r'$d=1/2r$')
    plt.xticks(x)
    plt.xlabel('轴向距离' + r'$ x/cm $')
    plt.yticks(np.arange(0, math.ceil(max(max(B_2R), max(B_halfR)))+1))
    plt.ylabel(r'$ B/mT $')
    plt.title('改变两圆线圈间距后轴线上磁场分布')
    plt.grid()
    plt.show()
table_2()