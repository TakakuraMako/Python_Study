import numpy as np

def ahp(matrix):
    # 计算特征值和特征向量
    eigenvalue, eigenvector = np.linalg.eig(matrix)
    # 提取最大特征值对应的特征向量，并归一化
    max_eigenvalue_index = np.argmax(eigenvalue)
    max_eigenvalue = eigenvalue[max_eigenvalue_index]
    weight = eigenvector[:, max_eigenvalue_index]
    weight = weight / np.sum(weight)
    return weight, max_eigenvalue

def consistency_check(matrix, weight):
    n = len(matrix)
    # 计算一致性指标 CI
    lambda_max = np.sum(np.dot(matrix, weight) / weight) / n
    CI = (lambda_max - n) / (n - 1)

    # 随机一致性指标 RI 的值，这里我们假设矩阵大小不超过10
    RI_list = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59, 1.61, 1.63, 1.64, 1.65]
    RI = RI_list[n - 1]

    # 计算一致性比例 CR
    CR = CI / RI
    return CI, CR

# 输入判断矩阵
matrix_1 = np.array([
        [1, 3, 5, 7],
        [1/3, 1, 4, 6],
        [1/5, 1/4, 1, 3],
        [1/7, 1/6, 1/3, 1],
    ])

# 计算判断矩阵的权重和最大特征值
weight_1, max_eigenvalue_1 = ahp(matrix_1)

# 检查一致性
CI1, CR1 = consistency_check(matrix_1, weight_1)

print("特征向量：")
print("Weight:", weight_1)
print("最大特征值：")
print("Max Eigenvalue:", max_eigenvalue_1)
print("CI值：")
print("CI:", CI1)
print("一致性检验结果：")
print("CR:", CR1)