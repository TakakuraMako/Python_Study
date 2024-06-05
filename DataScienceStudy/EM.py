import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

class GMM_EM:
    def __init__(self, n_components, max_iter=100, tol=1e-4):
        """
        高斯混合模型的EM算法初始化

        参数:
        n_components (int): 高斯分布的数量
        max_iter (int): 最大迭代次数
        tol (float): 收敛阈值
        """
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
    
    def fit(self, X):
        """
        使用EM算法拟合高斯混合模型

        参数:
        X (numpy.ndarray): 训练数据，形状为 (n_samples, n_features)
        """
        n_samples, n_features = X.shape

        # 初始化参数
        np.random.seed(0)
        self.means = X[np.random.choice(n_samples, self.n_components, False)]
        self.covariances = np.array([np.eye(n_features)] * self.n_components)
        self.weights = np.ones(self.n_components) / self.n_components

        log_likelihood = 0

        for iteration in range(self.max_iter):
            # E步：计算责任度
            responsibilities = self._estimate_responsibilities(X)

            # M步：更新参数
            self._maximization(X, responsibilities)

            # 检查收敛性
            new_log_likelihood = self._compute_log_likelihood(X)
            if np.abs(new_log_likelihood - log_likelihood) < self.tol:
                break
            log_likelihood = new_log_likelihood

    def _estimate_responsibilities(self, X):
        """
        计算E步中的责任度

        参数:
        X (numpy.ndarray): 数据，形状为 (n_samples, n_features)

        返回:
        responsibilities (numpy.ndarray): 责任度，形状为 (n_samples, n_components)
        """
        weighted_probs = np.zeros((X.shape[0], self.n_components))

        for k in range(self.n_components):
            # 计算每个分量的加权概率
            weighted_probs[:, k] = self.weights[k] * multivariate_normal.pdf(X, self.means[k], self.covariances[k])

        sum_probs = weighted_probs.sum(axis=1, keepdims=True)
        return weighted_probs / sum_probs

    def _maximization(self, X, responsibilities):
        """
        在M步中更新参数

        参数:
        X (numpy.ndarray): 数据，形状为 (n_samples, n_features)
        responsibilities (numpy.ndarray): 责任度，形状为 (n_samples, n_components)
        """
        Nk = responsibilities.sum(axis=0)

        # 更新均值
        self.means = (responsibilities.T @ X) / Nk[:, np.newaxis]
        # 更新权重
        self.weights = Nk / X.shape[0]

        for k in range(self.n_components):
            diff = X - self.means[k]
            # 更新协方差矩阵
            self.covariances[k] = (responsibilities[:, k][:, np.newaxis] * diff).T @ diff / Nk[k]

    def _compute_log_likelihood(self, X):
        """
        计算对数似然函数

        参数:
        X (numpy.ndarray): 数据，形状为 (n_samples, n_features)

        返回:
        log_likelihood (float): 对数似然值
        """
        log_likelihood = 0
        for k in range(self.n_components):
            log_likelihood += np.log(multivariate_normal.pdf(X, self.means[k], self.covariances[k]) * self.weights[k]).sum()
        return log_likelihood

    def predict(self, X):
        """
        使用拟合的模型对数据进行预测

        参数:
        X (numpy.ndarray): 数据，形状为 (n_samples, n_features)

        返回:
        labels (numpy.ndarray): 预测的标签，形状为 (n_samples,)
        """
        responsibilities = self._estimate_responsibilities(X)
        return np.argmax(responsibilities, axis=1)

# 生成示例数据
np.random.seed(0)
X1 = np.random.multivariate_normal([0, 0], [[1, 0], [0, 1]], 100)
X2 = np.random.multivariate_normal([5, 5], [[1, 0], [0, 1]], 100)
X = np.vstack([X1, X2])

# 拟合GMM模型
gmm = GMM_EM(n_components=2)
gmm.fit(X)

# 预测聚类标签
labels = gmm.predict(X)

# 绘制结果
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(gmm.means[:, 0], gmm.means[:, 1], c='red', marker='x')
plt.title('GMM Clustering using EM Algorithm')
plt.show()
