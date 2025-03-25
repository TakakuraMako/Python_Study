import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

data = pd.read_excel('./数据分析/沪深.xlsx')
# print(data.head())
# print(data.info())
# print(data.describe())
# 绘制每日最高最低价箱线图，收盘价在中间，折线图
plt.figure(figsize=(12, 6))
muti_data = [i in ['最高价', '最低价'] for i in data.columns]
muti_data.plot.box()
plt.title('沪深指数每日最高最低价箱线图')
plt.grid(True)
plt.show()
