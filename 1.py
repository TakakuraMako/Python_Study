import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 使plt支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data1 = pd.DataFrame([[35.22, 499.80], [10.41, 161.37], [17.22, 273.29], [10.70, 134.79],
                      [10.29, 90.92], [18.66, 348.99], [4.41, 106.89], [6.24, 196.44],
                      [49.72, 656.95], [47.70, 580.70], [36.55, 518.10], [14.85, 179.41],
                      [19.46, 250.16], [10.93, 122.06], [40.26, 552.74], [19.82, 268.20],
                      [19.49, 221.43], [16.01, 197.68], [99.32, 1080.26],[14.77, 160.60],
                      [3.96, 39.51], [10.49, 111.76], [21.71, 250.09], [13.06, 95.87],
                      [20.34, 183.62], [0.77, 6.08], [11.38, 133.50], [3.66, 64.86],
                      [1.21, 18.30],[2.31, 23.81], [3.24, 103.81]], columns=['11月', '1~11月'], index=range(1, 32))
x1_mean = round(data1.mean(), 2)
S1_2 = round(np.var(data1, ddof=1, axis=0), 2)
S1 = round(np.std(data1, ddof=1, axis=0), 2)
CV1 = round(x1_mean / S1, 2)
G31 = round(data1.skew(), 2)
G41 = round(data1.kurt(), 2)
M1 = data1.median()
Q11 = data1.quantile(0.25)
Q31 = data1.quantile(0.75)
IQR1 = Q31 - Q11
TM1 = 1/4*Q11 + 1/2*M1 + 1/4*Q31
# 画出经验分布函数图
# 计算经验分布函数的值
def empirical_distribution_function(data):
    n = len(data)
    sorted_data = np.sort(data)
    
    # 计算经验分布函数
    ecdf = np.arange(1, n + 1) / n
    return sorted_data, ecdf

# 获取排序的数据和对应的经验分布函数值
sorted_data, ecdf = empirical_distribution_function(data1.iloc[:, 0])

# 绘制经验分布函数曲线
plt.figure(figsize=(10, 6))
plt.step(sorted_data, ecdf, where='post', label='Empirical CDF', color='blue')
plt.title('Empirical Distribution Function (EDF)')
plt.xlabel('Data Value')
plt.ylabel('Empirical Probability')
plt.grid()
plt.legend()
plt.show()