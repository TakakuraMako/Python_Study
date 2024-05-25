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
'''
# 奖金区间
q = [50000, 35000, 23000, 11000, 5000, 0]

# 用于记录每个奖金区间的人数
line = np.zeros(5)

i = person
while i > 0:
    money = x / i
    for j in range(len(q) - 1):
        if q[j] >= money > q[j + 1]:
            line[j] += 1
            x = x - (q[j] + q[j + 1]) / 2
            break
    i -= 1

print(line)
'''
'''
#5% 10% 15% 20%
title = pd.DataFrame({
    '正高':[1, 1.1, 1.2, 1.3],
    '副高':[1/1.1, 1, 1.1, 1.2],
    '中级':[1/1.2, 1/1.1, 1, 1.1],
    '初级':[1/1.3, 1/1.2, 1/1.1, 1]
})

title = [[1, 1.1, 1.2, 1.3],[1/1.1, 1, 1.1, 1.2],[1/1.2, 1/1.1, 1, 1.1],[1/1.3, 1/1.2, 1/1.1, 1]]
weight = [0.28468769, 0.26033493, 0.2376522, 0.21732518]
attribute = []
money = []
ratio = [0.05, 0.15, 0.35]
for i in range(len(ratio)):
    num_person = math.floor(person * ratio[i])
    attribute.append(num_person)
    money.append(x / 3 / attribute[i])
print(attribute)
print(money)
'''

