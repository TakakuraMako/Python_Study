import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
# 读取小时销售数据的Excel文件
hour_data_path = 'hour_data销量(千克).xlsx'
hour_data = pd.read_excel(hour_data_path)

# 提取特征：计算每种蔬菜类别的平均值、标准差和最大值
# iloc[:, 1:] 表示选择除第一列以外的所有列（即各蔬菜类别的销售数据）
# agg(['mean', 'std', 'max']) 用于计算每种蔬菜类别的统计特征
# .T 表示将结果转置，使每行对应一个蔬菜类别，列为不同的特征
features = hour_data.iloc[:, 1:].agg(['mean', 'std', 'max']).T

# 标准化特征数据
# StandardScaler 用于将特征数据标准化（均值为0，方差为1）
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 应用层次聚类算法
# AgglomerativeClustering 创建一个层次聚类模型对象
# n_clusters=None 表示不预先指定聚类的数量，distance_threshold=0 表示构建完整的层次树
clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0)
clustering.fit(scaled_features)

# 将聚类结果（标签）添加到特征数据中
features['Cluster'] = clustering.labels_

# 按照聚类标签对特征数据进行排序，方便查看同一聚类中的类别
features_with_clusters = features.sort_values(by='Cluster')

# 使用中文字体并生成树状图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 生成树状图（dendrogram），并将横坐标标签改为蔬菜类别名称
plt.figure(figsize=(10, 7))

# linkage矩阵用于描述各个样本之间的聚合关系
linked = sch.linkage(scaled_features, method='ward')

# 生成树状图，并指定标签为原始数据中的蔬菜类别名称
dendrogram = sch.dendrogram(linked, labels=features.index, leaf_rotation=90)

plt.title('树状图')
plt.xlabel('蔬菜类别')
plt.ylabel('欧几里得距离')
plt.show()
