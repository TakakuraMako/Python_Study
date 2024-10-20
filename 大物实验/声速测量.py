from sympy import *
def table1():
    t = 23
    v = 331.37 * sqrt(1 + t / 237.15)
    x1 = [15.1, 19.6, 24.2, 28.64, 33.50, 38.3, 43.00, 47.56, 52.3, 56.94]
    x2 = [103.92, 108.5, 113.24, 117.42, 122.46, 127.26, 131.9, 136.4, 141.18, 145.7]
    x_delta = []
    for i in range(len(x1)):
        x_delta.append(round(x2[i] - x1[i], 2))
    x_d_average = sum(x_delta) / 10
    lambda_average = x_d_average / 10
    sums = 0
    for i in range(len(x1)):
        sums += (x_delta[i] - x_d_average) ** 2
    S_x = sqrt(sums / 9)
    delta_a = 0.72 * S_x
    delta_b = 0.01
    delta_x = sqrt(delta_a**2 + delta_b**2)
    delta_lambda = delta_x / 10
    f = 37360
    v_average = f * x_d_average * 10**-4
    v_delta = v_average * sqrt((3/f)**2 + (delta_lambda / lambda_average)**2)
    U_r = v_delta / v_average
    r = abs(v - v_average) / v
    print('delta = x_i+20 - x_i = {} \ndelta的均值={} \ndelta标准差={} \ndelta_A={}mm \ndelta_B={}mm \ndelta_x={} \nv_average={} \nv_delta_average={} \n相对不确定度U_r={}\n相对误差r={}'.format(x_delta, x_d_average, S_x, delta_a, delta_b, delta_x, v_average, v_delta, U_r, r))

def table2():
    t = 23
    v = 331.37 * sqrt(1 + t / 237.15)
    x1 = [3, 12.26, 21.48, 30.9, 40.2, 49.48, 59, 68.3, 77.86, 87.1]
    x2 = [96.62, 105.59, 115.4, 124.6, 133.94, 143.28, 153.0, 162.32, 171.1, 180.46]
    dx = []
    for i in range(len(x1)):
        dx.append(round(x2[i] - x1[i], 2))
    x_d_average = sum(dx) / 10
    lambda_average = x_d_average / 10
    sums = 0
    for i in range(len(x1)):
        sums += (dx[i] - x_d_average) ** 2
    S_x = sqrt(sums / 9)
    delta_a = 0.72 * S_x
    delta_b = 0.01
    delta_x = sqrt(delta_a**2 + delta_b**2)
    delta_lambda = delta_x / 10
    f = 37360
    v_average = f * x_d_average * 10**-4
    v_delta = v_average * sqrt((3/f)**2 + (delta_lambda / lambda_average)**2)
    U_r = v_delta / v_average
    r = abs(v - v_average) / v
    print('delta = x_i+10 - x_i ={}\nx_d_average={}\nlambda_average={}\nS_x={}\ndelta_A={}\ndelta_B={}\ndelta_x={}\ndelta_lambda={}\nv_average={}\nv_delta_average={}\n相对不确定度U_r={}\n相对误差r={}'.format(dx,x_d_average, lambda_average, S_x, delta_a, delta_b, delta_x, delta_lambda, v_average, v_delta, U_r, r))

table1()