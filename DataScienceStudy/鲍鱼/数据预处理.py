import pandas as pd
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import numpy as np
plt.rcParams['font.sans-serif'] = 'SimHei' #解决图标中文
plt.rc('axes', unicode_minus=False)   #解决 UserWarning: Glyph 8722 (\N{MINUS SIGN}) missing from current font.问题

data = pd.read_csv("C:/Document/university/code/Python/数据科学/鲍鱼/abalone_dataset.csv")
#sex的onehot编码
sex_onehot = pd.get_dummies(data['sex'], prefix='sex')
data[sex_onehot.columns] = sex_onehot
print(data.head(2))
#添加取值为 1 的特征
data['ones'] = 1

#计算年龄
data['age'] = data['rings'] + 1.5
y = data['age']

#构造两组特征集
features_with_ones = ["length","diameter","height","whole_weight","shucked_weight","viscera_weight","shell_weight","sex_F","sex_M","ones"]
features_without_ones=["length","diameter","height","whole_weight","shucked_weight","viscera_weight","shell_weight","sex_F","sex_M"]
X = data[features_with_ones]


#将鲍鱼数据集划分为训练集和测试集
X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,test_size=0.2, random_state=111)

#线性回归-numpy
def linear_regression(X,y):
    w = np.zeros_like(X.shape[1])
    if np.linalg.det(X.T.dot(X).astype(float)) != 0 :
        w = np.linalg.inv(X.T.dot(X).astype(float)).dot(X.T).dot(y)#inv只能是float类型，注意转换
    return w

w1 = linear_regression(X_train,y_train)
w1 = pd.DataFrame(data = w1,index = X.columns,columns = ["numpy_w"])
w1.round(decimals=2)

#线性回归-sklearn
lr = linear_model.LinearRegression()
lr.fit(X_train[features_without_ones],y_train)
w_lr = []
w_lr.extend(lr.coef_)
w_lr.append(lr.intercept_)
w1["lr_sklearn_w"] = w_lr
w1.round(decimals=2)

#在训练集上训练鲍鱼年龄预测模型时，使用 Numpy 实现的线性回归模型与 sklearn 得到的结果是一致的

#使用 Numpy 实现岭回归 (Ridge)
def ridge_regression(X,y,ridge_lambda):
    penalty_matrix = np.eye(X.shape[1])
    penalty_matrix[X.shape[1] - 1][X.shape[1] - 1] = 0
    w = np.linalg.inv(X.T.dot(X).astype(float) + ridge_lambda * penalty_matrix).dot(X.T).dot(y)
    return w

w2 = ridge_regression(X_train,y_train,1.0)
w1["numpy_ridge_w"] = w2
w1.round(decimals=2)

#使用 sklearn 实现岭回归 (Ridge)
ridge = linear_model.Ridge(alpha=1.0)
ridge.fit(X_train[features_without_ones],y_train)
w_ridge = []
w_ridge.extend(ridge.coef_)
w_ridge.append(ridge.intercept_)
w1["ridge_sklearn_w"] = w_ridge
w1.round(decimals=2)
print(w1)

#使用 LASSO 构建鲍鱼年龄预测模型
lasso = linear_model.Lasso(alpha=0.01)
lasso.fit(X_train[features_without_ones],y_train)
print(lasso.coef_)
print(lasso.intercept_)

#鲍鱼年龄预测模型效果评估
y_test_pred_lr = lr.predict(X_test.iloc[:,:-1])
print(round(mean_absolute_error(y_test,y_test_pred_lr),4))

y_test_pred_ridge = ridge.predict(X_test[features_without_ones])
print(round(mean_absolute_error(y_test,y_test_pred_ridge),4))

y_test_pred_lasso = lasso.predict(X_test[features_without_ones])
print(round(mean_absolute_error(y_test,y_test_pred_lasso),4))
print(round(r2_score(y_test,y_test_pred_lr),4))
print(round(r2_score(y_test,y_test_pred_ridge),4))
print(round(r2_score(y_test,y_test_pred_lasso),4))

#残差图
plt.figure(figsize=(9, 6))
y_train_pred_ridge = ridge.predict(X_train[features_without_ones])
plt.scatter(y_train_pred_ridge, y_train_pred_ridge - y_train, c="g", alpha=0.6)
plt.scatter(y_test_pred_ridge, y_test_pred_ridge - y_test, c="r",alpha=0.6)
plt.hlines(y=0, xmin=0, xmax=30,color="b",alpha=0.6)
plt.ylabel("Residuals")
plt.xlabel("Predict")

#岭迹
alphas = np.logspace(-10,10,20)
coef = pd.DataFrame()
for alpha in alphas:
    ridge_clf = Ridge(alpha=alpha)
    ridge_clf.fit(X_train[features_without_ones],y_train)
    df = pd.DataFrame([ridge_clf.coef_],columns=X_train[features_without_ones].columns)
    df['alpha'] = alpha
    coef = coef._append(df,ignore_index=True)#此处应为_append否则报错
print(coef.head().round(decimals=2))
#绘图
#plt.rcParams['figure.dpi'] = 1000 #分辨率
plt.figure(figsize=(9, 6))
coef['alpha'] = coef['alpha']

for feature in X_train.columns[:-1]:
    plt.plot('alpha',feature,data=coef)
ax = plt.gca()
ax.set_xscale('log')
plt.legend(loc='upper right')
plt.xlabel(r'$\alpha$',fontsize=15)
plt.ylabel('系数',fontsize=15)

plt.show()

#LASSO 的正则化路径
coef = pd.DataFrame()
for alpha in np.linspace(0.0001,0.2,20):
    lasso_clf = Lasso(alpha=alpha)
    lasso_clf.fit(X_train[features_without_ones],y_train)
    df = pd.DataFrame([lasso_clf.coef_],columns=X_train[features_without_ones].columns)
    df['alpha'] = alpha
    coef = coef._append(df,ignore_index=True)
coef.head()
#绘图
plt.figure(figsize=(9, 6))
for feature in X_train.columns[:-1]:
    plt.plot('alpha',feature,data=coef)
plt.legend(loc='upper right')
plt.xlabel(r'$\alpha$',fontsize=15)
plt.ylabel('系数',fontsize=15)
plt.show()
