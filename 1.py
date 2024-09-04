import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False

data = pd.DataFrame({'乘机服务':[71, 84, 84, 87, 72, 72, 72, 63, 84, 90, 72, 94, 84, 85, 88, 74, 71, 88, 90, 85, 79, 72, 88, 77, 64, 72, 71, 69, 90, 84, 86, 70, 86, 87, 77, 71, 75, 74, 76, 95, 89, 85, 65, 82, 82, 89, 74, 82, 90, 78],
                     '机上服务':[49, 53, 74, 66, 59, 37, 57, 48, 60, 62, 56, 60, 42, 56, 55, 70, 45, 49, 27, 89, 59, 60, 36, 60, 43, 76, 25, 47, 56, 28, 37, 38, 72, 51, 90, 36, 53, 59, 51, 66, 66, 57, 42, 37, 60, 80, 47, 49, 76, 52],
                     '到达机场服务':[58, 63, 37, 49, 79, 86, 40, 78, 29, 66, 55, 52, 66, 64, 52, 51, 68, 42, 67, 46, 41, 45, 47, 75, 61, 37, 74, 16, 23, 62, 59, 54, 72, 57, 51, 55, 92, 82, 54, 52, 62, 67, 68, 54, 56, 64, 63, 91, 70, 72]})

data = pd.DataFrame(data, index=range(50))

# 绘图
plt.figure(figsize=(15, 5))

# 乘机服务
plt.subplot(1, 3, 1)
plt.hist(data['乘机服务'], bins=10, color='skyblue', edgecolor='black')
plt.xticks(range(0, 101, 10))
plt.title('乘机服务')
plt.xlabel('评分')
plt.ylabel('频数')

# 机上服务
plt.subplot(1, 3, 2)
plt.hist(data['机上服务'], bins=10, color='lightgreen', edgecolor='black')
plt.xticks(range(0, 101, 10))
plt.title('机上服务')
plt.xlabel('评分')
plt.ylabel('频数')

# 到达机场服务
plt.subplot(1, 3, 3)
plt.hist(data['到达机场服务'], bins=10, color='salmon', edgecolor='black')
plt.xticks(range(0, 101, 10))
plt.title('到达机场服务')
plt.xlabel('评分')
plt.ylabel('频数')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
data.boxplot(column=['乘机服务', '机上服务', '到达机场服务'])
plt.title('三个指标的箱线图')
plt.ylabel('评分')
plt.grid(False)
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', cbar=True, square=True, fmt='.2f')
plt.title('相关性热力图')
plt.show()