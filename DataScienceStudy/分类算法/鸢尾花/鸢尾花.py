import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv('DataScienceStudy\分类算法\鸢尾花\iris.csv')
X = data.drop(['Id', 'Species'], axis=1)
y = data['Species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 数据标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# SVM 模型
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)
svm_predictions = svm_model.predict(X_test)

# Logistics 回归模型
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)
logistic_predictions = logistic_model.predict(X_test)

# 性能评估
svm_accuracy = accuracy_score(y_test, svm_predictions)
logistic_accuracy = accuracy_score(y_test, logistic_predictions)

print(f"SVM Accuracy: {svm_accuracy}")
print(f"Logistic Regression Accuracy: {logistic_accuracy}")

# 详细分类报告
print("Classification report for SVM:")
print(classification_report(y_test, svm_predictions))

print("Classification report for Logistic Regression:")
print(classification_report(y_test, logistic_predictions))