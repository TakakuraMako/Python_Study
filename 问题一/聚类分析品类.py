import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import numpy as np
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False
# 读取上传的Excel文件
file_path_weekly = './问题一/单品日销量处理.xlsx'

# 从Excel文件中读取数据
df_weekly = pd.read_excel(file_path_weekly)

# 将销售日期转换为日期格式，并创建一个“周”列，表示该日期所在的周
df_weekly['销售日期'] = pd.to_datetime(df_weekly['销售日期'])
earliest_date = df_weekly['销售日期'].min()

# 计算每个日期相对于最早日期的第几周
df_weekly['周数'] = ((df_weekly['销售日期'] - earliest_date).dt.days // 7) + 1

# 按品类名称和自定义的周数进行分组，并计算每周的总销量
df_weekly_grouped_custom = df_weekly.groupby(['品类名称', '周数'])['销量(千克)'].sum().reset_index()

# 数据预处理：将每个品类的每周销量数据转换为矩阵形式
pivot_df = df_weekly_grouped_custom.pivot(index='品类名称', columns='周数', values='销量(千克)').fillna(0)

# 计算距离矩阵，这里使用欧氏距离
distance_matrix = pdist(pivot_df, metric='euclidean')

# 使用层次聚类方法（例如平均链）进行聚类
Z = linkage(distance_matrix, method='average')

# 绘制聚类树状图（dendrogram）
plt.figure(figsize=(10, 7))
dendrogram(Z, labels=pivot_df.index, leaf_rotation=90)
plt.title('品类销量的层次聚类树状图')
plt.xlabel('品类名称')
plt.ylabel('欧氏距离')
plt.show()
