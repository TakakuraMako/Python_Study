import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib.font_manager import FontProperties

matplotlib.rc("font",family='MicroSoft YaHei',weight="bold")
# 读取Excel文件
file_path = './数模/A题：附件1.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 删除“序号”和“职称”列，因为它们不是数值特征
data = df.drop(columns=['序号', '职称'])

# 标准化数据
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# 执行 PCA，保留所有主成分
pca = PCA()
principal_components = pca.fit_transform(scaled_data)


# 确定累计解释方差比例超过 0.85 的主成分数量
cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
k = np.argmax(cumulative_variance_ratio >= 0.85) + 1

# 选择前 k 个主成分
selected_eigenvectors = pca.components_[:k]
principal_components_selected = principal_components[:, :k]

# 创建包含主成分的数据框
pca_df = pd.DataFrame(data=principal_components_selected, columns=[f'PC{i+1}' for i in range(k)])
pca_df['序号'] = df['序号']

# 计算因子载荷矩阵
# 因子载荷矩阵 = 标准化数据 * 选定的特征向量
loadings_matrix = selected_eigenvectors.T * np.sqrt(pca.explained_variance_[:k])

# 创建因子载荷矩阵的数据框
loadings_df = pd.DataFrame(data=loadings_matrix, columns=[f'PC{i+1}' for i in range(k)], index=data.columns)

# 计算最终得分
final_scores = np.dot(principal_components_selected, pca.explained_variance_ratio_[:k])
pca_df['FinalScore'] = final_scores
# 映射最终得分到0-100
min_score = pca_df['FinalScore'].min()
max_score = pca_df['FinalScore'].max()
pca_df['MappedScore'] = 100 * (pca_df['FinalScore'] - min_score) / (max_score - min_score)

# 根据最终得分进行排名
pca_df['Rank'] = pca_df['FinalScore'].rank(ascending=False).astype('int32')
pca_df = pca_df.sort_values(by='Rank')

# 输出因子载荷矩阵和最终得分
print("因子载荷矩阵：")
print(loadings_df)
print("\n主成分分析结果：")
print(pca_df[['序号', 'MappedScore', 'Rank']])