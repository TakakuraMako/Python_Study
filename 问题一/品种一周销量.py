import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False
# 读取品种一周销量数据
file_path = './问题一/品种一周销量.xlsx'
data = pd.read_excel(file_path)

# 将数据透视，以“销售日期”为索引，“单品名称”为列，值为“销量(千克)”
pivot_data = data.pivot_table(index='星期几', columns='分类名称', values='销量(千克)', aggfunc='sum')

# 折线图
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(11, 5))
for column in list(pivot_data.columns):
    plt.plot(pivot_data.index, pivot_data[column], label=column)

plt.title('品种的一周销量折线图')
plt.xlabel('星期')
plt.ylabel('销量（千克）')
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()
