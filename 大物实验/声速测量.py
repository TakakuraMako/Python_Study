from sympy import *
def table1():
    t = 23
    x1 = [15.1, 19.6, 24.2, 28.64, 33.50, 38.3, 43.00, 47.56, 52.3, 56.94]
    x2 = [103.92, 108.5, 113.24, 117.42, 122.46, 127.26, 131.9, 136.4, 141.18, 145.7]
    x_delta = []
    for i in range(len(x1)):
        x_delta.append(round(x2[i] - x1[i], 2))
    x_d_average = sum(x_delta)/10
    sums = 0
    for i in range(len(x1)):
        sums += (x_delta[i] - x_d_average) ** 2
    S_x = sqrt(sums / 9)

    print('delta = x_i+20 - x_i = {} \ndelta的均值={} \ndelta标准差={}'.format(x_delta, x_d_average, S_x))

def table2():
    x1 = [30.2, 41.08, 50.14, 59.68, 69.16, 78.34, 87.46, 91.1, 106.12, 115.12]
    x2 = [122.54, 133.92, 143.32, 152.86, 161.7, 170.6, 180.02, 183.20, 198.58, 207.70]
    dx = [92.34, 92.84, 92.96, 93.18, 92.54, 92.26, 92.56, 92.1, 92.38, 92.58]
    sum = 0
    for i in range(len(dx)):
        sum += dx[i]
    dx_average = (round(sum / 10, 2))
    temp = 0
    for i in range(len(dx)):
        temp += (dx_average - dx[i])**2
    S_x = round(sqrt(temp / 9), 4)
    print(S_x)
    print(331.21*sqrt(1+22.5/237.15))

table1()