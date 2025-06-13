import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 读取数据
df = pd.read_excel('./数据分析/大作业/清洗后数据.xlsx')

# 选取数值特征
numeric_cols = ['LIMIT_BAL','AGE'] + \
               ['PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6'] + \
               [f'BILL_AMT{i}' for i in range(1,7)] + \
               [f'PAY_AMT{i}' for i in range(1,7)]

X = df[numeric_cols]

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 1. 主成分分析（PCA）
pca = PCA(n_components=len(numeric_cols))
X_pca = pca.fit_transform(X_scaled)

# 可视化累计解释方差
explained = pca.explained_variance_ratio_
cum_explained = explained.cumsum()

plt.figure(figsize=(6,4))
plt.plot(range(1, len(explained)+1), cum_explained, marker='o')
plt.axhline(0.9, linestyle='--', color='red')
plt.title('累计解释方差比例')
plt.xlabel('主成分数')
plt.ylabel('累计解释方差')
plt.grid(True)
plt.tight_layout()
plt.show()

# 前两主成分投影散点图
plt.figure(figsize=(6,5))
plt.scatter(X_pca[:,0], X_pca[:,1], s=10, alpha=0.5)
plt.title('前两主成分散点')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.tight_layout()
plt.show()

# 2. 聚类分析（KMeans）
# 肘部法则选择簇数
inertia = []
ks = range(1,11)
for k in ks:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_pca[:,:10])  # 基于前10主成分聚类
    inertia.append(km.inertia_)

plt.figure(figsize=(6,4))
plt.plot(ks, inertia, marker='o')
plt.title('KMeans 肘部图')
plt.xlabel('簇数 k')
plt.ylabel('Inertia')
plt.grid(True)
plt.tight_layout()
plt.show()

# 选 k=6
k = 6
km3 = KMeans(n_clusters=k, random_state=42)
clusters = km3.fit_predict(X_pca[:,:10])
df['cluster'] = clusters

# 每簇样本数
print("各簇样本数：")
print(df['cluster'].value_counts())

# 每簇违约率
print("\n各簇违约率：")
print(df.groupby('cluster')['default payment next month'].mean())

# 前五期逾期均值对比
print("\n各簇 PAY_0 平均值：")
print(df.groupby('cluster')['PAY_0'].mean())
