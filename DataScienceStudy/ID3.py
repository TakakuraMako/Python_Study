import numpy as np
import pandas as pd
import math

data = pd.read_csv('./DataScienceStudy/西瓜数据集 2.0.csv')
print(data.head())
print(data.shape)
epsilon = 2
lables = ['色泽','根蒂','敲声','纹理','脐部','触感','好瓜']
lables_count = {'色泽':{},'根蒂':{},'敲声':{},'纹理':{},'脐部':{},'触感':{},'好瓜':{}}
rows = data.shape[0]
for i in lables:#统计各种性状的数量，放入字典
    for index,x in data.iterrows():
        if x[i] not in lables_count[i]:
            lables_count[i][x[i]] = dict.fromkeys(['是','否','num'],0)
        if x[-1] == '是':
            lables_count[i][x[i]]['是'] += 1
        else:
            lables_count[i][x[i]]['否'] += 1
        lables_count[i][x[i]]['num'] += 1



def Calculate_H(lables):
    H = 0
    for i in lables_count[lables].values():
        H -= i/(rows-1) * math.log2(i/(rows-1))
    return H

H_D = np.array([])#储存每个类的熵
for i in lables:
    H_D = np.append(H_D, Calculate_H(i))
print(H_D)
