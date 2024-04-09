import numpy as np
import pandas as pd
import math
import tree
import copy

data = pd.read_csv('./DataScienceStudy/分类算法/西瓜数据集 2.0.csv')
epsilon = 2
lables = ['色泽','根蒂','敲声','纹理','脐部','触感']
lables_count_init = {'色泽':{},'根蒂':{},'敲声':{},'纹理':{},'脐部':{},'触感':{}}


def Calcualate_num(lables,data, lables_count_init):
    lables_count_temp = copy.deepcopy(lables_count_init)
    
    for i in lables:#统计各种性状的数量，放入字典
        for index,x in data.iterrows():
            if x[i] not in lables_count_temp[i]:
                lables_count_temp[i][x[i]] = dict.fromkeys(['是','否','num'],0)
            if x.iloc[-1] == '是':
                lables_count_temp[i][x[i]]['是'] += 1
            else:
                lables_count_temp[i][x[i]]['否'] += 1
            lables_count_temp[i][x[i]]['num'] += 1
    return lables_count_temp


def Calcualate_H(data):
    result = dict.fromkeys(['是','否'],0)
    result['否'] = data['好瓜'].value_counts()['否']
    result['是'] = data['好瓜'].value_counts()['是']
    H_D = 0
    for i in result.values():
        H_D -= i/data.shape[0] * math.log2(i/data.shape[0])
    return H_D

def Calclate_H_D_A(lables, lables_count, data):
    H_D_A = dict.fromkeys(lables_count,0)
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
    return H_D_A

def Calclate_G_D_A(data, lables, lables_count):
    H_D = Calcualate_H(data)
    #print('H_D:{0}'.format(H_D))
    lables_count = Calcualate_num(lables, data, lables_count_init)
    H_D_A = Calclate_H_D_A(lables, lables_count, data)
    G_D_A = dict.fromkeys(lables_count,0)
    for i in lables:
        G_D_A[i] = H_D - H_D_A[i]
    #print(G_D_A)
    insert = max(G_D_A, key=lambda x: G_D_A[x])
    #print(insert)

    for i in lables_count[insert]:
        if lables_count[insert][i]['是'] == 0:
            print('no'+ i)
        elif lables_count[insert][i]['否'] == 0:
            print('yes'+ i)

        else:
            data_new = data
            lables_new =copy.deepcopy(lables)
            lables_new.remove(insert)
            for a,x in data.iterrows():
                if x[insert] != i:
                    data_new = data_new.drop(a)
            lables_count_init_new = copy.deepcopy(lables_count_init)
            lables_count_init_new.pop(insert)
            #print(data_new)
            Calclate_G_D_A(data_new, lables_new, lables_count_init_new)

Calclate_G_D_A(data, lables, lables_count_init)
