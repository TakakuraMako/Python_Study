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
            lables_count[i][x[i]] = 0
        lables_count[i][x[i]] += 1



def Calculate_H(lables):
    H = 0
    for i in lables_count[lables].values():
        H -= i/(rows-1) * math.log2(i/(rows-1))
    return H

H_D = np.array([])#储存每个类的熵
for i in lables:
    H_D = np.append(H_D, Calculate_H(i))
print(H_D)

H_D_A = np.array([])#条件熵
for i in lables_count.values():
    for j in i.values():

