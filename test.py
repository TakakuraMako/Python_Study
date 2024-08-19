import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
path2 = '附件2.xlsx'

data2 = pd.read_excel(path2)

# 将日期列转换为日期类型
data2['销售日期'] = pd.to_datetime(data2['销售日期'])

# 提取星期几（0表示星期一，6表示星期日）
data2['星期几'] = data2['销售日期'].dt.dayofweek+1

# 计算每周七天的销量
weekly_sales = data2.groupby(['分类名称','星期几'])['销量(千克)'].sum().reset_index()
weekly_sales.to_excel('品种一周销量.xlsx')
# plt.rcParams['font.family'] = 'simhei'
# plt.rcParams['axes.unicode_minus'] = False
# plt.title("净藕(1)箱线图")
# plt.boxplot(data_dan_hourly.iloc[:, 1])
# plt.xlabel('销量')
# plt.show()

# q1 = data2.iloc[:, 3].quantile(q=0.25)
# q3 = data2.iloc[:, 3].quantile(q=0.75)
# IQR = (q3-q1)*1.5
# low = q1 - IQR
# up = q3 + IQR
# for index, row in data2.iloc[:, 3:4].iterrows():
#     if row['销量(千克)'] >= up or row['销量(千克)'] <= low:
#         data2 = data2.drop(index=index)
# data2.to_excel('new附件2.xlsx')

# week_data = pd.DataFrame({'花叶类':0, '花菜类':0, '水生根茎类':0, '茄类':0, '辣椒类':0, '食用菌':0},index=range(1,8))
# month_data = pd.DataFrame({'花叶类':0, '花菜类':0, '水生根茎类':0, '茄类':0, '辣椒类':0, '食用菌':0},index=range(1,13))
# hour_data = pd.DataFrame({'花叶类':0, '花菜类':0, '水生根茎类':0, '茄类':0, '辣椒类':0, '食用菌':0},index=range(0,24))
# for index, row in data2.iterrows():
#     date_str = str(row['销售日期']).split(' ')[0]
#     print(date_str)
#     date_obj = datetime.strptime(date_str, "%Y-%m-%d")
#     hour_num = int(row['扫码销售时间'].split(':')[0])
#     weekday_num = int(date_obj.weekday()) + 1
#     month_num = int(date_obj.month)
#     week_data.loc[weekday_num,row['分类名称']] += row['销量(千克)']
#     month_data.loc[month_num,row['分类名称']] += row['销量(千克)']
#     hour_data.loc[hour_num,row['分类名称']] += row['销量(千克)']
# week_data.to_excel('week_data销量(千克).xlsx',index=False)
# month_data.to_excel('month_data销量(千克).xlsx',index=False)
# hour_data.to_excel('hour_data销量(千克).xlsx',index=False)

