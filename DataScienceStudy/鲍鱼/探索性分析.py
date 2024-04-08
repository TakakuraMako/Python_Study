import pandas as pd
import warnings
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
data = pd.read_csv("./数据科学/鲍鱼/abalone_dataset.csv")
print(data.head())
print(data.shape)


plt.figure(num=1)
sns.countplot(x = "sex", data = data)

i = 1 # 子图记数
plt.figure(figsize=(16, 8))
for col in data.columns[1:]:
    plt.subplot(4,2,i)
    i = i + 1
    sns.histplot(data[col],kde=True,color='deepskyblue',edgecolor='none')  
plt.tight_layout()#自动调整子图像参数

sns.pairplot(data,hue="sex")#两两之间的特征关系

'''
#pandas2.0版本后，原来corr函数自动忽略字符串等非浮点数的特性被修改。现在需要加上numeric_only=True才会忽略字符串
'''
corr_df = data.corr(numeric_only=True)#相关系数矩阵
fig, ax = plt.subplots(figsize=(16, 16))
## 绘制热力图
ax = sns.heatmap(corr_df,linewidths=.5,cmap="Greens",annot=True,xticklabels=corr_df.columns, yticklabels=corr_df.index)
ax.xaxis.set_label_position('top') 
ax.xaxis.tick_top()


plt.show()
