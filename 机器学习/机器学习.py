import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('./机器学习/用户用电数据/RAW_House5_Part2.csv')
#查看基本信息
'''
print(data.head)
print(data.info())
print(data.shape)
print(data.describe())
'''
#和时间有关，向前填充
print(np.any(data.isnull()))
#data.fillna(method='ffill')
#data.fillna(method='bfill')
