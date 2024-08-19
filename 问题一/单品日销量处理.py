import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 随机选择几个单品
df = pd.read_excel('./问题一/单品日销量.xlsx')
sample_products = df['单品名称'].sample(5, random_state=42).unique()

plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False
# 为每个选中的单品绘制箱线图
plt.figure(figsize=(10, 6))
for product in sample_products:
    product_data = df[df['单品名称'] == product]['销量(千克)']
    plt.boxplot(product_data, positions=[np.where(sample_products == product)[0][0]], widths=0.6)
    
plt.xticks(ticks=np.arange(len(sample_products)), labels=sample_products, rotation=45)
plt.title("随机选择的单品销量箱线图")
plt.ylabel("销量(千克)")
plt.show()

# 替换异常值为单品的销量均值
def replace_outliers_with_mean(group):
    q1 = group.quantile(0.25)
    q3 = group.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    mean_value = group.mean()
    
    return group.apply(lambda x: mean_value if x < lower_bound or x > upper_bound else x)

df['销量(千克)'] = df.groupby('单品名称')['销量(千克)'].transform(replace_outliers_with_mean)

df.to_excel('单品日销量处理.xlsx')
