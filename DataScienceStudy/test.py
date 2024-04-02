import numpy as np
import pandas as pd
import math
data = pd.read_csv('./DataScienceStudy/西瓜数据集 2.0.csv')
lables = ['色泽','根蒂','敲声','纹理','脐部','触感','好瓜']
lables_count = {'色泽':{'青绿':2},'根蒂':{},'敲声':{},'纹理':{},'脐部':{},'触感':{},'好瓜':{}}

for i in lables:#统计各种性状的数量，放入字典
    for index,x in data.iterrows():
        if x[i] not in lables_count[i]:
            lables_count[i][x[i]] = 0
        lables_count[i][x[i]] += 1

#计算总体熵
H = 0
rows = data.shape[0]
for i in lables_count['好瓜'].values():
    H -= i/(rows-1) * math.log2(i/(rows-1))
print(H)