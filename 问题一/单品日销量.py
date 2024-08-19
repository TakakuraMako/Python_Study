import pandas as pd
import matplotlib.pyplot as plt
import random
path = './问题一/单品日销量.xlsx'
data = pd.read_excel(path)

# 将数据透视，以“销售日期”为索引，“单品名称”为列，值为“销量(千克)”
pivot_data = data.pivot_table(index='销售日期', columns='单品名称', values='销量(千克)', aggfunc='sum')
# 随机选择五个单品名称
random_samples = random.sample(list(pivot_data.columns), 1)

# 绘制随机选择的单品的日销量折线图
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False
for column in random_samples:
    plt.plot(pivot_data.index, pivot_data[column], label=column)

plt.figure(figsize=(14, 7))
for column in random_samples:
    plt.plot(pivot_data.index, pivot_data[column], label=column)

plt.title('随机选择的10个单品的日销量折线图')
plt.xlabel('日期')
plt.ylabel('销量（千克）')
plt.legend(loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 输出随机选择的单品名称
print("随机选择的单品:", random_samples)