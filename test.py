import numpy as np
import torch
import matplotlib.pyplot as plt

# 创建一个模拟数据集
data = torch.tensor([[25, 5, 50],[30, 3, 40],[35, 1, 20],[40,4,30],[45,6,35],[65,3,30]], dtype=torch.float32)

# 初始化K个中心点
K = 3
centers = data[torch.randperm(data.shape[0])][:K]

# KMeans算法主体
for i in range(10):  # 迭代10次
    # 步骤2：计算每个点到各个中心点的距离，并分配到最近的中心点
    distances = torch.cdist(data, centers)
    labels = torch.argmin(distances, dim=1)

    # 步骤3：重新计算中心点
    for k in range(K):
        centers[k] = data[labels == k].mean(dim=0)

# 结果可视化
plt.scatter(data[:, 0], data[:, 1], c=labels)
plt.scatter(centers[:, 0], centers[:, 1], marker='x')
plt.show()
