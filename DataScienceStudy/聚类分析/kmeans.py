import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# 读取数据
iris = load_iris()
data = pd.DataFrame(iris['data'], columns=iris['feature_names'])

# 数据标准化
data_zs = (data - data.mean()) / data.std()

# 初始化质心
def initialize_centroids(data, k):
    return data.sample(n=k).values

# 分配样本到质心
def assign_clusters(data, centroids):
    distances = np.linalg.norm(data.values[:, np.newaxis] - centroids, axis=2)
    return np.argmin(distances, axis=1)

# 更新质心
def update_centroids(data, labels, k):
    return np.array([data[labels == i].mean(axis=0) for i in range(k)])

# K-means算法实现
def kmeans(data, k, max_iters=100):
    centroids = initialize_centroids(data, k)
    for _ in range(max_iters):
        labels = assign_clusters(data, centroids)
        new_centroids = update_centroids(data, labels, k)
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    return labels, centroids

# 手肘法确定K值
sse = []
k_values = range(1, 10)
for k in k_values:
    labels, centroids = kmeans(data_zs, k)
    # 计算总的SSE
    total_sse = np.sum(np.min(np.linalg.norm(data_zs.values[:, np.newaxis] - centroids, axis=2), axis=1) ** 2)
    sse.append(total_sse)

# 绘制手肘法图形
plt.figure(figsize=(8, 4))
plt.plot(k_values, sse, marker='x')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Sum of Squared Errors (SSE)')
plt.title('Elbow Method for Optimal k')
plt.grid(True)
plt.show()
# 根据手肘法选择最佳K值
best_k = 3  # 通过观察图形确定的最佳K值

# 运行K-means并可视化结果
labels, centroids = kmeans(data_zs, best_k)

# 可视化结果
plt.figure(figsize=(8, 6))
plt.scatter(data.values[:, 0], data.values[:, 1],c=labels, cmap='viridis')
#plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, alpha=0.75)
plt.xlabel(iris['feature_names'][0])
plt.ylabel(iris['feature_names'][1])
plt.title('K-means Clustering')
plt.grid(True)



