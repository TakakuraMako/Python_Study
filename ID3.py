import numpy as np
import pandas as pd
data = pd.read_csv('数据科学/分类算法/西瓜数据集 2.0.csv')
print(data.head())
print(data.shape)
epsilon = 2
lable = ['色泽','根蒂','敲声','纹理','脐部','触感','好瓜']

def Calculate_H(lable):
    H = 0
    lable_counts = {}#没出现就放进字典
    #统计特征数量
    for i in data.iterrows():#遍历每一行
        for j in range(len(lable)):
            if i[j] not in lable_counts:
                lable_counts[j] = 0
            lable_counts[j] += 1

    return lable_counts

lable_counts = Calculate_H(lable)
print(lable_counts)