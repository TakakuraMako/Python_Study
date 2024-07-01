import numpy as np
from scipy.optimize import linprog

# 定义参数
M = 50000  # 基金初始金额（单位：万元）
n = 10     # 总年数

# 定期存款利率
r = {
    1: 0.018,
    2: 0.01944,
    3: 0.0216,
    5: 0.02304
}

# 转化成邻接矩阵，使用-ln(1 + r)作为权重
def create_weight_matrix(n, r):
    W = np.full((n + 1, n + 1), np.inf)
    for i in range(n):
        for k, rate in r.items():
            if i + k <= n:
                W[i, i + k] = -np.log(1 + rate * k)
    return W

W = create_weight_matrix(n, r)

# 利用Bellman-Ford算法求最短路径
def bellman_ford(W, start):
    n = W.shape[0]
    dist = np.full(n, np.inf)
    pred = np.full(n, -1)
    dist[start] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if W[u, v] != np.inf and dist[u] + W[u, v] < dist[v]:
                    dist[v] = dist[u] + W[u, v]
                    pred[v] = u

    # 检查负权重循环
    for u in range(n):
        for v in range(n):
            if W[u, v] != np.inf and dist[u] + W[u, v] < dist[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    return dist, pred

dist, pred = bellman_ford(W, 0)

# 构建路径
path = []
i = n
while i != -1:
    path.append(i)
    i = pred[i]
path = path[::-1]

# 最短路径对应的利率乘积最大
ri = [np.exp(-W[path[i], path[i + 1]]) for i in range(len(path) - 1)]

# 构建线性规划问题
c = [-1] * len(ri)  # 目标是最大化A，因此取负值
A_eq = np.zeros((1, len(ri)))
b_eq = np.zeros(1)

# 建立约束条件
for i in range(len(ri)):
    A_eq[0, i] = ri[i]

# 最后一年的约束条件
b_eq[0] = M

bounds = [(0, None)] * len(ri)

# 求解线性规划问题
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if res.success:
    x = res.x
    A = ri[0] * x[0]
    print(f"每年的奖金金额为: {A:.2f} 万元")
    print("分配情况为:")
    for i in range(len(x)):
        print(f"第 {path[i]} 年存入 {x[i]:.2f} 万元")
else:
    print("无法找到最优解")
