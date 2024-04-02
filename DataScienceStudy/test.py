import numpy as np
import pandas as pd
import math
data = pd.read_csv('./DataScienceStudy/西瓜数据集 2.0.csv')
lables = ['色泽','根蒂','敲声','纹理','脐部','触感','好瓜']
#lables_count = dict.fromkeys(lables,[[]],)
lables_count = {'色泽':{},'根蒂':{},'敲声':{},'纹理':{},'脐部':{},'触感':{},'好瓜':{}}

for i in lables:#统计各种性状的数量，放入字典
    for index,x in data.iterrows():
        if x[i] not in lables_count[i]:
            lables_count[i][x[i]] = dict.fromkeys(['是','否','num'],0)
        if x[-1] == '是':
            lables_count[i][x[i]]['是'] += 1
        else:
            lables_count[i][x[i]]['否'] += 1
        lables_count[i][x[i]]['num'] += 1

print(lables_count)