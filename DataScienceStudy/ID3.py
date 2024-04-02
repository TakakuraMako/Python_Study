import numpy as np
import pandas as pd

data = pd.read_csv('./DataScienceStudy/西瓜数据集 2.0.csv')
print(data.head())
print(data.shape)
epsilon = 2
lables = ['色泽','根蒂','敲声','纹理','脐部','触感','好瓜']
lables_count = {'色泽','根蒂','敲声','纹理','脐部','触感','好瓜'}
def Calculate_H(lables):
    H = 0
    for i in lables:#统计各种性状的数量，放入字典
        num = 0
        for index,x in data.iterrows():
            if x[i] not in lables_count[num][x[i]]:
                lables_count[num][x[i]] = 0
            lables_count[num][x[i]] += 1
        num += 1

    return lable_counts

lable_counts = Calculate_H(lables)
print(lable_counts)