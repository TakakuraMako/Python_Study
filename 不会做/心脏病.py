import pandas as pd # 数据处理
import numpy as np # 使用数组
import matplotlib.pyplot as plt # 可视化
from matplotlib import rcParams # 图大小
from termcolor import colored as cl # 文本自定义

from sklearn.tree import DecisionTreeClassifier as dtc # 树算法
from sklearn.model_selection import train_test_split # 拆分数据
from sklearn.metrics import accuracy_score # 模型准确度
from sklearn.tree import plot_tree # 树图

rcParams['figure.figsize'] = (25, 20)

data = pd.read_csv('./不会做/cardio_train.csv')
data = data.drop(columns='id')

X_var = data[['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']].values
Y_var = data[['cardio']].values

X_train, X_test, Y_train, Y_test = train_test_split(X_var, Y_var, test_size = 0.2, random_state = 0)

model = dtc(criterion = 'entropy', max_depth = 4)
model.fit(X_train, Y_train)

pred_model = model.predict(X_test)

feature_names = data.columns[:10]
target_names = data['cardio'].unique().tolist()

for i in range(len(target_names)):
    target_names[i] = str(target_names[i])

plot_tree(model, feature_names = feature_names, class_names = target_names, filled = True, rounded = True)
plt.savefig('tree_visualization.png') 