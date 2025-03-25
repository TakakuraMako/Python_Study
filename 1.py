import numpy as np
a = np.array([74, 78, 85, 88, 94, 80, 70, 85, 90, 85])
# 样本方差
s2 = np.sum((a - np.mean(a))**2) / (len(a) - 1)
# 样本标准差
std = np.sqrt(s2)
# 变异系数
cv = std / np.mean(a) * 100
# 极差
r = np.max(a) - np.min(a)
# 四分位极差
q3, q1 = np.percentile(a, [75, 25])
R1 = q3 - q1
# 四分位标准差
Q = R1/1.349
# 分析异常值
print(a[(a < q1 - 1.5 * R1) | (a > q3 + 1.5 * R1)])
print(s2, std, cv, r, R1, Q)