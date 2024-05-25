import numpy as np
import math
import pandas as pd
# 初始奖金总额和人数
x = 44444.44

money = []
data = pd.read_excel('./pca1.xlsx')
person = data.shape[0]
for i in range(person):
    money.append(round(data.iloc[i,-2]/data['MappedScore'].sum()*x,2))
print(money)
print(sum(money))