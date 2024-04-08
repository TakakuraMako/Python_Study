import numpy as np
import pandas as pd
import math
import tree

data = pd.read_csv('./DataScienceStudy/西瓜数据集 2.0.csv')
epsilon = 2
lables = ['色泽','根蒂','敲声','纹理','脐部','触感']
lables_count = {'色泽':{},'根蒂':{},'敲声':{},'纹理':{},'脐部':{},'触感':{}}


def Calcualate_num(lables,data,lables_count):
    for i in lables:#统计各种性状的数量，放入字典
        for index,x in data.iterrows():
            if x[i] not in lables_count[i]:
                lables_count[i][x[i]] = dict.fromkeys(['是','否','num'],0)
            if x.iloc[-1] == '是':
                lables_count[i][x[i]]['是'] += 1
            else:
                lables_count[i][x[i]]['否'] += 1
            lables_count[i][x[i]]['num'] += 1
    return lables_count


def Calcualate_H(data):
    result = dict.fromkeys(['是','否'],0)
    result['否'] = data['好瓜'].value_counts()['否']
    result['是'] = data['好瓜'].value_counts()['是']
    H_D = 0
    for i in result.values():
        H_D -= i/data.shape[0] * math.log2(i/data.shape[0])
    return H_D

def Calclate_H_D_A():
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
            H_D_A[i] += lables_count[i][x]['num']/data.shape[0]*H

while True:
    H_D = Calcualate_H(data)
    lables_count = Calcualate_num(lables, data, lables_count)

    H_D_A = dict.fromkeys(lables_count,0)
    G_D_A = dict.fromkeys(lables_count,0)


        G_D_A[i] = H_D - H_D_A[i]
    print(G_D_A)
    insert = max(G_D_A, key=lambda x: G_D_A[x])
    print(insert)
    lables_count.pop(insert)
    lables.remove(insert)
    data.drop(columns=insert)
    for a,x in data.iterrows():
        print(x[insert])
        if x[insert] == '清晰':
            data = data.drop(a)
    print(data)
    if len(lables_count) == 0:
        break



