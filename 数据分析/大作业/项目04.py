import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 1. 读取清洗后数据
df = pd.read_excel('./数据分析/大作业/清洗后数据.xlsx')
target = 'default payment next month'

# 2. 异方差修正：对额度、账单和还款金额使用 Yeo-Johnson 变换（可处理负值）
skew_cols = ['LIMIT_BAL'] + [f'BILL_AMT{i}' for i in range(1,7)] + [f'PAY_AMT{i}' for i in range(1,7)]
pt = PowerTransformer(method='yeo-johnson', standardize=False)
df[skew_cols] = pt.fit_transform(df[skew_cols])

# 3. 共线性修正：PCA 降维账单与还款（基于变换后的同一列）
bill_pay_cols = [f'BILL_AMT{i}' for i in range(1,7)] + [f'PAY_AMT{i}' for i in range(1,7)]
scaler_bp = StandardScaler()
X_bp = scaler_bp.fit_transform(df[bill_pay_cols])
pca = PCA(n_components=2, random_state=42)
bp_pca = pca.fit_transform(X_bp)
df['PC_bill'], df['PC_payamt'] = bp_pca[:,0], bp_pca[:,1]
df.drop(columns=bill_pay_cols, inplace=True)

# 4. 构建特征与标签
feature_cols = [
    'LIMIT_BAL','AGE',
    'PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6',
    'PC_bill','PC_payamt',
    'SEX','EDUCATION','MARRIAGE'
]
X = pd.get_dummies(df[feature_cols], drop_first=True)
y = df[target]

# 5. 标准化所有特征
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. 分割训练/测试集
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# 7. 训练带 L2 正则和平衡类别权重的逻辑回归
model = LogisticRegressionCV(
    penalty='l2',
    solver='liblinear',
    class_weight='balanced',
    cv=5,
    max_iter=1000
)
model.fit(X_train, y_train)

# 8. 评估逻辑回归
y_pred = model.predict(X_test)
print("=== 逻辑回归评估 ===")
print(classification_report(y_test, y_pred, zero_division=0))
print("混淆矩阵：")
print(confusion_matrix(y_test, y_pred))

# 9. 聚类分析：基于预测概率
df['pred_prob'] = model.predict_proba(scaler.transform(X))[:,1]
kmeans = KMeans(n_clusters=3, random_state=42)
df['risk_cluster'] = kmeans.fit_predict(df[['pred_prob']])

# 10. 聚类汇总与可视化
cluster_summary = df.groupby('risk_cluster').agg(
    count=('SEX','size'),
    mean_prob=('pred_prob','mean'),
    default_rate=(target,'mean')
).sort_values('mean_prob')

print("\n=== 风险聚类汇总 ===")
print(cluster_summary)

cluster_summary[['mean_prob','default_rate']].plot.bar(figsize=(6,4))
plt.title('风险聚类：预测概率 vs 实际违约率')
plt.xlabel('风险簇')
plt.ylabel('比例')
plt.xticks(rotation=0)
plt.legend(['平均预测概率','实际违约率'])
plt.tight_layout()
plt.show()
