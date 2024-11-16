import numpy as np
import math
def table1():
    d = [5.0, 5.309, 5.611, 5.948, 6.217, 6.526]
    delta_d_list = []
    delta_d_ave = 0
    for i in range(3):
        delta_d_list.append((d[i+3] - d[i]) / 3 * 10**-3)
        delta_d_ave += (d[i+3] - d[i]) / 9 * 10**-3
    print(f'delta_d_ave={delta_d_ave}m')
    lambda_ave = 2 * delta_d_ave / 50 / 20
    print(f'lambda_ave={lambda_ave}m')
    print(f'delta_d={delta_d_list}')
    S = np.std(delta_d_list)
    print(f'标准差={S}m')
    delta_A_d = 2.48 * S
    delta_B_d = 0.004 * 10 **-3
    delta_d = math.sqrt(delta_A_d**2 + delta_B_d**2)
    print(f'delta_A_d={delta_A_d}m')
    print(f'delta_d={delta_d}m')
    delta_lambda = 2 * delta_d / 50 / 20
    print(f'delta_lambda={delta_lambda}m')

def table2():
    N = [16, 17, 16, 17, 17]
    delta_p = [200, 210, 200, 208, 210]
    n = []
    p = 760
    L = 0.08
    lamda = 623.8 * 10**-9
    for i in range(len(N)):
        n.append(round(1 + N[i] * lamda / 2 / L * p / delta_p[i], 6))
    print(n)
    print(np.average(n))
table2()