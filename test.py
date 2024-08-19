import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
'''
path1 = 'C:/Users/13619/Downloads/C题/附件1.xlsx'
data1 = pd.read_excel(path1)
print(data1.head())
'''
path2 = 'C:/Users/13619/Downloads/C题/附件2.xlsx'
data2 = pd.read_excel(path2)
#print(data2.iloc[:, 3:5].describe())

plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False

plt.subplot(121)
plt.title("默认样式")
plt.boxplot(data2.iloc[:, 3])



print(data2.iloc[:, 3:5].quantile(q=[0.25, 0.75]))
q1 = data2.iloc[:, 3].quantile(q=0.25)
q3 = data2.iloc[:, 3].quantile(q=0.75)

IQR = (q3-q1)*1.5
low = q1 - IQR
up = q3 + IQR
for index, row in data2.iloc[:, 3:4].iterrows():
    if row['销量(千克)'] >= up or row['销量(千克)'] <= low:
        data2 = data2.drop(index=index)


print(data2.shape)
plt.subplot(121)
plt.title("默认样式")
plt.boxplot(data2.iloc[:, 3])
plt.show()