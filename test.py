import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
'''
path1 = '附件1.xlsx'
data1 = pd.read_excel(path1)
print(data1.head())
'''
path2 = '附件2.xlsx'
data2 = pd.read_excel(path2)
#print(data2.iloc[:, 3:5].describe())
data2 = data2.iloc[0:2000, :]
#data2.to_excel('new附件2.xlsx', index=False)
'''
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False

plt.title("默认样式")
plt.boxplot(data2.iloc[:, 3])
plt.show()
'''

print(data2.iloc[:, 3:5].quantile(q=[0.25, 0.75]))
q1 = data2.iloc[:, 3].quantile(q=0.25)
q3 = data2.iloc[:, 3].quantile(q=0.75)

IQR = (q3-q1)*1.5
low = q1 - IQR
up = q3 + IQR
for index, row in data2.iloc[:, 3:4].iterrows():
    if row['销量(千克)'] >= up or row['销量(千克)'] <= low:
        data2 = data2.drop(index=index)

week_data = pd.DataFrame({'花叶类':0, '花菜类':0, '水生根茎类':0, '茄类':0, '辣椒类':0, '食用菌':0},index=range(1,8))
for index, row in data2.iterrows():
    date_str = str(row['销售日期']).split(' ')[0]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday_num = int(date_obj.weekday())
    week_data.iloc[weekday_num][row['分类名称']] += 1
print(week_data)
week_data.to_excel('week_data.xlsx')

'''
#计算每天品类销量
data = pd.DataFrame({'花叶类':0, '花菜类':0, '水生根茎类':0, '茄类':0, '辣椒类':0, '食用菌':0},index=[0])
for index, row in data2.iterrows():
    data[row['品类']] += 1
print(data)
'''