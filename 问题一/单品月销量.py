import pandas as pd
import matplotlib.pyplot as plt
import random
# 读取单品月销量数据
monthly_file_path = './问题一/单品月销量.xlsx'
monthly_sales_data = pd.read_excel(monthly_file_path)

# 将数据透视，以“销售月份”为索引，“单品名称”为列，值为“销量(千克)”
monthly_pivot_data = monthly_sales_data.pivot_table(index='月', columns='单品名称', values='销量(千克)', aggfunc='sum')

# 随机选择五个单品名称
random_monthly_samples = random.sample(list(monthly_pivot_data.columns), 10)

# 绘制随机选择的十个单品的月销量折线图
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(14, 7))
for column in random_monthly_samples:
    plt.plot(monthly_pivot_data.index, monthly_pivot_data[column], label=column)

plt.title('随机选择的十个单品的月销量折线图')
plt.xlabel('月份')
plt.ylabel('销量（千克）')
plt.legend(loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 输出随机选择的单品名称
random_monthly_samples
