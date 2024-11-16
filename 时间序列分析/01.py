import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 读取数据
file_path = './时间序列分析/北京日均气温2000-2023.xlsx'
data = pd.read_excel(file_path)

# 将'Date'列转换为日期格式，并设置为索引
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 步骤1：直接过滤低于-20度的气温数据
data_cleaned = data[data['AverageTemperature'] > -19.6]

# 步骤2：按月计算每月的均值和标准差，使用3-Sigma方法
data_cleaned['Month'] = data_cleaned.index.to_period('M')
monthly_stats = data_cleaned.groupby('Month')['AverageTemperature'].agg(['mean', 'std']).reset_index()
monthly_stats.columns = ['Month', 'MeanTemp', 'StdTemp']

# 将每月的统计数据合并回原始数据，应用3-Sigma规则筛选数据
data_cleaned = data_cleaned.reset_index().merge(monthly_stats, on='Month', how='left')
data_cleaned = data_cleaned[(data_cleaned['AverageTemperature'] >= data_cleaned['MeanTemp'] - 3 * data_cleaned['StdTemp']) &
                            (data_cleaned['AverageTemperature'] <= data_cleaned['MeanTemp'] + 3 * data_cleaned['StdTemp'])]

# 再次将' Date'列设置为索引
data_cleaned.set_index('Date', inplace=True)

# 绘制每日温度图，空缺值不显示
plt.figure(figsize=(12, 6))
plt.plot(data_cleaned['AverageTemperature'], marker='.', linestyle='-', markersize=2, alpha=0.7)
plt.title('每日平均气温（清洗后）')
plt.xlabel('日期')
plt.ylabel('气温 (°C)')
plt.grid(True)
plt.show()

# 绘制2001年每个月的箱线图
data_2001 = data_cleaned[data_cleaned.index.year == 2001]
data_2001['Month'] = data_2001.index.month  # 添加‘Month’列便于分组

plt.figure(figsize=(12, 6))
data_2001.boxplot(column='AverageTemperature', by='Month')
plt.title('2001年每月温度箱线图')
plt.suptitle('')  # 移除默认标题
plt.xlabel('月')
plt.ylabel('温度(°C)')
plt.grid(True)
plt.show()

# 步骤3：基于3-Sigma清洗后的data_cleaned，使用IQR方法进一步去除异常值
data_cleaned['Month'] = data_cleaned.index.month  # 按月分组处理

# 定义IQR过滤函数
def filter_outliers_iqr(df, value_col, group_col):
    Q1 = df.groupby(group_col)[value_col].transform(lambda x: x.quantile(0.25))
    Q3 = df.groupby(group_col)[value_col].transform(lambda x: x.quantile(0.75))
    IQR = Q3 - Q1
    return df[(df[value_col] >= Q1 - 1.5 * IQR) & (df[value_col] <= Q3 + 1.5 * IQR)]

# 应用IQR过滤
data_filtered = filter_outliers_iqr(data_cleaned, 'AverageTemperature', 'Month')
data_filtered = data_filtered[['AverageTemperature']]  # 保留必要的列
# 绘制每日温度图，空缺值不显示
plt.figure(figsize=(12, 6))
plt.plot(data_filtered['AverageTemperature'], marker='.', linestyle='-', markersize=2, alpha=0.7)
plt.title('每日平均气温（清洗后）')
plt.xlabel('日期')
plt.ylabel('气温 (°C)')
plt.grid(True)
plt.show()
data_interpolated = data_filtered.interpolate(method='linear')
