import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
'''
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
'''
# N分别为3, 7, 13, 15, 19，每一行N相同 
T_withAl = np.array([[2.5257, 2.5031, 2.4796, 2.5110, 2.5224],
                     [4.6260, 4.6000, 4.5785, 4.6086, 4.6155],
                     [6.8930, 6.8672, 6.8548, 6.8861, 6.8927],
                     [7.6447, 7.6192, 7.6123, 7.6430, 7.6459],
                     [9.1603, 9.1352, 9.1399, 9.1690, 9.1752]])

T_withoutAl = np.array([[1.6100, 1.6103, 1.6299, 1.6308, 1.6287],
                        [2.9677, 2.9727, 2.9958, 2.9905, 2.9967],
                        [4.44472, 4.4529, 4.4833, 4.4743, 4.9834],
                        [4.9404, 4.9454, 4.9790, 4.9688, 4.9834],
                        [5.9367, 5.9403, 5.9802, 5.9675, 5.9864]])

def Caculate_J(T):
    # 每行求平均得到对应的平均时间
    T_average = np.mean(T, axis=1)
    print(f"所测平均时间为{T_average}")
    theta1_prime = 2 * np.pi
    theta2_prime = 6 * np.pi
    t1_prime = round(T_average[3] - T_average[2], 4)
    t2_prime = round(T_average[4] - T_average[2], 4)
    print(f"t1\'={t1_prime}, t2\'={t2_prime}")
    beta_prime = round(2*(theta1_prime * t2_prime - theta2_prime * t1_prime) / (t1_prime**2 * t2_prime - t1_prime * t2_prime**2), 4)
    print(f"β\'={beta_prime}")
    t1 = round(T_average[0], 4)
    t2 = round(T_average[1], 4)
    theta1 = 2 * np.pi
    theta2 = 6 * np.pi
    print(f"t1={t1}, t2={t2}")
    beta = round(2*(theta1 * t2 - theta2 * t1) / (t1**2 * t2 - t1 * t2**2), 4)
    print(f"β={beta}")
    m = 0.03 #kg
    r = 0.03 #m
    g = 9.8 #m/s2
    J = round(m * g * r / (beta - beta_prime), 7)
    print(f"J={J}")
    return J

def Method1():
    print("计算有铝盘的J")
    J_withAl = Caculate_J(T_withAl)

    print("\n计算没有铝盘的J")
    J_withoutAl = Caculate_J(T_withoutAl)

    print("\n计算铝盘的J")
    J_Al = J_withAl - J_withoutAl
    print(J_Al)

    # 理论值
    m_prime = 437.50 * 10**(-3) # kg
    R = 0.12 # m
    J_theory = m_prime * R**2 / 2
    print(f"\nJ理论={J_theory}")
    
    # 相对误差
    relative_error = (J_Al - J_theory) / J_theory
    print(f"相对误差={relative_error}")

# Method1()

def Nihe(t_n2, m):
    # 最小二乘法拟合
    model = LinearRegression()
    model.fit(t_n2.reshape(-1, 1), m.reshape(-1, 1))
    # 生成预测值
    m_pred = model.predict(t_n2.reshape(-1, 1))
    print(f"斜率K={model.coef_}")
    print(f"截距mu={model.intercept_}")
    theta = 6 * np.pi
    r = 0.03 # m
    g = 9.8
    J = model.coef_ * g * r / 2 / theta
    print(f"J={J}")
    plt.figure()
    plt.scatter(t_n2, m)
    plt.plot(t_n2, m_pred)
    plt.xlim(0, max(t_n2) + 0.01)
    plt.ylim(0, max(m_pred) + 0.005)
    plt.grid()
    plt.title(r'无铝盘时$m$与$1/t^2$的关系')
    plt.xlabel(r'$1/t^2$')
    plt.ylabel(r'$m$')
    plt.show()
    return J
def Method2():
    # 质量
    _m = np.arange(15, 51, 5)
    m = np.array([x * 10**-3 for x in _m])

    # 带盘和不带盘时间
    t_withAl = np.array([7.2255, 6.1769, 5.4640, 4.9766, 4.6008, 4.2536, 4.0372, 3.8450])
    t_withoutAl = np.array([4.5936, 3.9928, 3.5346, 3.2277, 2.9865, 2.7947, 6418, 2.4816])

    # 时间倒数平方
    t_withAl_n2 = np.array([round(1 / (x**2), 4) for x in t_withAl])
    t_withoutAl_n2 = np.array([round(1 / (x**2), 4) for x in t_withoutAl])
    print("带铝盘")
    J = Nihe(t_withAl_n2, m)
    print(f"\n不带铝盘")
    J_0 = Nihe(t_withoutAl_n2, m)
    J_x = J - J_0
    # 理论值
    m_prime = 437.50 * 10**(-3) # kg
    R = 0.12 # m
    J_theory = m_prime * R**2 / 2
    print(f"\nJ理论={J_theory}")
    # 相对误差
    relative_error = (J_x - J_theory) / J_theory
    print(f"相对误差={relative_error}")
Method2()