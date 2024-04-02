import numpy as np
import pandas as pd
import math
data = pd.read_csv('./DataScienceStudy/西瓜数据集 2.0.csv')
lables = ['色泽','根蒂','敲声','纹理','脐部','触感']
#lables_count = dict.fromkeys(lables,[[]],)
lables_count = {'色泽':{},'根蒂':{},'敲声':{},'纹理':{},'脐部':{},'触感':{}}
result = dict.fromkeys(['是','否'],0)
for i in lables:#统计各种性状的数量，放入字典
    for index,x in data.iterrows():
        if x[i] not in lables_count[i]:
            lables_count[i][x[i]] = dict.fromkeys(['是','否','num'],0)
        if x.iloc[-1] == '是':
            lables_count[i][x[i]]['是'] += 1
            result['是'] += 1
        else:
            lables_count[i][x[i]]['否'] += 1
            result['否'] += 1
        lables_count[i][x[i]]['num'] += 1
result['否'] /= data.shape[1]-2
result['是'] /= data.shape[1]-2

H_D = 0
for i in result.values():
    H_D -= i/data.shape[0] * math.log2(i/data.shape[0])

H_D_A = dict.fromkeys(lables,0)
G_D_A = dict.fromkeys(lables,0)
for i in lables:
    ls = list(lables_count[i].keys())#每一种性状的具体属性
    for x in ls:#每一个具体属性的熵
        H = 0
        p_i = lables_count[i][x]['是']/lables_count[i][x]['num']
        if p_i != 0:
            H -= p_i * math.log2(p_i)
        p_i = lables_count[i][x]['否']/lables_count[i][x]['num']
        if p_i != 0:
            H -= p_i * math.log2(p_i)
        H_D_A[i] -= lables_count[i][x]['num']/data.shape[0]*H
        G_D_A[i] = H_D - H_D_A[i]
print(G_D_A)
