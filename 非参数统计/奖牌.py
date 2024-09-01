import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimSun'] #宋体
plt.rcParams['axes.unicode_minus'] = False 
path = './非参数统计/奥运会奖牌榜.xlsx'
data = pd.read_excel(path)
gold = data[['Country','Gold']]
gold = gold[gold['Gold'] != 0]
bins = range(0, max(gold['Gold']) + 5, 5)

plt.figure()
plt.hist(gold['Gold'], bins=bins,edgecolor='black', alpha=0.7)
plt.xlabel('金牌')
plt.ylabel('数量')
plt.xticks(bins)
plt.show()