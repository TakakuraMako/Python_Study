import numpy as np
import matplotlib.pyplot as plt
# 使plt支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
a = np.array([7, 180, 85, 88, 94, 80, 70, 85, 90, 85])
plt.figure()
#绘制箱线图 
plt.boxplot(a,sym='o', meanline=True, showmeans=True, showcaps=True, showbox=True, showfliers=True, notch=False, patch_artist=False, vert=True, whis=1.5)
# 获取统计数据
q1 = np.percentile(a, 25)  # 下四分位数
q3 = np.percentile(a, 75)  # 上四分位数
iqr = q3 - q1              # 四分位极差
lower_bound = q1 - 1.5 * iqr  # 下截点
upper_bound = q3 + 1.5 * iqr  # 上截点
#plt.ylim(lower_bound, upper_bound)
# 标注上下截点
plt.text(1.1, lower_bound, f'下截点: {lower_bound:.1f}', color='purple')
plt.text(1.1, upper_bound, f'上截点: {upper_bound:.1f}', color='purple')

# 标注其他统计数据
plt.text(1.1, np.mean(a), f'均值: {np.mean(a):.1f}', color='blue')
plt.text(1.1, np.median(a), f'中位数: {np.median(a):.1f}', color='green')
plt.text(1.1, q1, f'Q1: {q1:.1f}', color='orange')
plt.text(1.1, q3, f'Q3: {q3:.1f}', color='orange')

plt.title('箱线图（带上下截点标注）')
plt.show()


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