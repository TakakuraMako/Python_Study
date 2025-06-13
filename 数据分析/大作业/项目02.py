import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from scipy.stats import norm
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 读取数据
df = pd.read_excel('./数据分析/大作业/清洗后数据.xlsx', header=0)

# 2. 相关分析：数值特征与目标的皮尔森相关系数
pay_cols = ['PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6']
numeric_cols = ['LIMIT_BAL','AGE'] + pay_cols + [f'BILL_AMT{i}' for i in range(1,7)] + [f'PAY_AMT{i}' for i in range(1,7)]
target = 'default payment next month'

corr = df[numeric_cols + [target]].corr()[target].drop(target)
plt.figure(figsize=(8,6))
corr.sort_values().plot.barh()
plt.title('数值特征与违约标签的相关系数')
plt.xlabel('Pearson 相关系数')
plt.tight_layout()
plt.show()

# 3. 构建逻辑回归模型
# 独热编码
X = pd.get_dummies(df[['SEX','EDUCATION','MARRIAGE'] + numeric_cols], drop_first=True)
y = df[target]

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# 训练模型
model = LogisticRegression(solver='liblinear', max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]

# 4. 模型评估
print("分类报告：")
print(classification_report(y_test, y_pred, zero_division=0))
print("混淆矩阵：")
print(confusion_matrix(y_test, y_pred))

# 绘制 ROC 曲线
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
plt.plot([0,1],[0,1],'--', color='gray')
plt.title('ROC 曲线')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.tight_layout()
plt.show()

# 5. 残差检验
residuals = y_test - y_prob

# 残差直方图
plt.figure(figsize=(6,4))
plt.hist(residuals, bins=30)
plt.title('残差直方图')
plt.xlabel('残差（实际 - 预测概率）')
plt.ylabel('频数')
plt.tight_layout()
plt.show()

# 残差 vs 预测值
plt.figure(figsize=(6,4))
plt.scatter(y_prob, residuals, s=10, alpha=0.5)
plt.axhline(0, linestyle='--', color='red')
plt.title('残差与拟合值散点图')
plt.xlabel('预测概率')
plt.ylabel('残差')
plt.tight_layout()
plt.show()

# Q-Q 图
res_sorted = np.sort(residuals)
theoretical_q = norm.ppf((np.arange(1, len(res_sorted)+1)-0.5)/len(res_sorted))
plt.figure(figsize=(6,4))
plt.scatter(theoretical_q, res_sorted, s=10)
plt.plot(theoretical_q, theoretical_q, '--', color='gray')
plt.title('残差 Q-Q 图')
plt.xlabel('理论分位数')
plt.ylabel('样本残差分位数')
plt.tight_layout()
plt.show()
