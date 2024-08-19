import numpy as np
import pandas as pd
path1 = "C:/Users/Mako/Downloads/C题/附件1.xlsx"
path2 = "C:/Users/Mako/Downloads/C题/附件2.xlsx"
'''
dict = {'花叶类':[], '花菜类':[], '水生根茎类':[], '茄类':[], '辣椒类':[], '食用菌':[]}
data1 = pd.read_excel(path1)
for i in range(data1.shape[0]):
    num = data1.iloc[i][0]
    type = data1.iloc[i][3]
    dict[type].append(num)
    print(dict)
    '''

data2 = pd.read_excel(path2)
print(data2.iloc[:,3:4].describe())