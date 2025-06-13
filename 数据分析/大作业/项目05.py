# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    classification_report,
    roc_auc_score,
    confusion_matrix
)
import numpy as np

# 1. 直接读取预先清洗好的数据
df = pd.read_excel('./数据分析/大作业/清洗后数据.xlsx')

# 标签列
y = df['default payment next month']

# ——以下都是特征工程、建模与评估——

# 2. 数值特征 Yeo–Johnson 变换
num_feats = ['LIMIT_BAL'] + [f'BILL_AMT{i}' for i in range(1,7)] + [f'PAY_AMT{i}' for i in range(1,7)]
pt = PowerTransformer(method='yeo-johnson')
df[num_feats] = pt.fit_transform(df[num_feats])

# 3. 项目03：基于前10个主成分的聚类分析
pca10 = PCA(n_components=10, random_state=42)
X_pca10 = pca10.fit_transform(df[num_feats])

# 3.1 KMeans 聚类 & 质量指标
n_clusters_03 = 4
km3 = KMeans(n_clusters=n_clusters_03, random_state=42)
labels03 = km3.fit_predict(X_pca10)
sil03 = silhouette_score(X_pca10, labels03)
ch03  = calinski_harabasz_score(X_pca10, labels03)
db03  = davies_bouldin_score(X_pca10, labels03)

# 3.2 各簇实际违约率
rate03 = pd.Series(y.values).groupby(labels03).mean()

print("=== 项目03 聚类分析 ===")
print(f"簇数 = {n_clusters_03}")
print(f"Silhouette = {sil03:.4f}   Calinski–Harabasz = {ch03:.1f}   Davies–Bouldin = {db03:.4f}")
print("各簇实际违约率：")
print(rate03)

# 4. 项目04：特征工程 + 最优逻辑回归模型
# 4.1 PCA 提取账单与还款两大主成分
pca2 = PCA(n_components=2, random_state=42)
bills_pays = [f'BILL_AMT{i}' for i in range(1,7)] + [f'PAY_AMT{i}' for i in range(1,7)]
cp = pca2.fit_transform(df[bills_pays])
df['PC_bill'], df['PC_payamt'] = cp[:,0], cp[:,1]
df.drop(columns=bills_pays, inplace=True)

# 4.2 类别独热编码
X = pd.get_dummies(df.drop(columns='default payment next month'), columns=['SEX','EDUCATION','MARRIAGE'], drop_first=True)

# 4.3 特征标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4.4 划分数据集
X_tr, X_te, y_tr, y_te = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# 4.5 训练 LogisticRegressionCV（L2 + balanced）
lr = LogisticRegressionCV(
    Cs=10, cv=5,
    scoring='roc_auc',
    class_weight='balanced',
    max_iter=1000,
    random_state=42
)
lr.fit(X_tr, y_tr)

# 4.6 基础模型评估
y_pred  = lr.predict(X_te)
y_proba = lr.predict_proba(X_te)[:,1]
auc_base = roc_auc_score(y_te, y_proba)

print("\n=== 项目04 最优逻辑回归模型 ===")
print(f"AUC = {auc_base:.4f}")
print("分类报告：")
print(classification_report(y_te, y_pred))
print("混淆矩阵：")
print(confusion_matrix(y_te, y_pred))

# 5. 项目04：基于全特征的风险分层聚类
n_clusters_04 = 3
km4 = KMeans(n_clusters=n_clusters_04, random_state=42)
labels04 = km4.fit_predict(X_scaled)
sil04 = silhouette_score(X_scaled, labels04)
ch04  = calinski_harabasz_score(X_scaled, labels04)
db04  = davies_bouldin_score(X_scaled, labels04)
rate04 = pd.Series(y.values).groupby(labels04).mean()

print("\n=== 项目04 风险分层聚类 ===")
print(f"簇数 = {n_clusters_04}")
print(f"Silhouette = {sil04:.4f}   Calinski–Harabasz = {ch04:.1f}   Davies–Bouldin = {db04:.4f}")
print("各风险等级违约率：")
print(rate04)

# 6. 将风险簇标签作为新特征，重训模型
df_feat = np.hstack([X_scaled, labels04.reshape(-1,1)])
X_tr2, X_te2, y_tr2, y_te2 = train_test_split(
    df_feat, y, test_size=0.3, random_state=42, stratify=y
)
lr2 = LogisticRegressionCV(
    Cs=10, cv=5,
    scoring='roc_auc',
    class_weight='balanced',
    max_iter=1000,
    random_state=42
)
lr2.fit(X_tr2, y_tr2)
y_proba2 = lr2.predict_proba(X_te2)[:,1]
auc_enh = roc_auc_score(y_te2, y_proba2)
print(f"\n加入风险簇特征后 AUC 提升至 = {auc_enh:.4f}")
