import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
# 加载数据
file_path = './时间序列分析/北京月均气温.xlsx'  # 修改为实际文件路径
temperature_data = pd.read_excel(file_path)

# 将 "Time" 列转换为日期类型并设置为索引
temperature_data['Time'] = pd.to_datetime(temperature_data['Time'])
temperature_data.set_index('Time', inplace=True)
def original_plot():
    plt.figure(figsize=(12, 6))
    plt.plot(temperature_data, label='月均温度')
    plt.xlabel('日期')
    plt.ylabel('温度 (°C)')
    plt.title('北京月均温度')
    plt.gca().set_xlim([temperature_data.index.min(), pd.Timestamp('2024-12-31')])
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))

    # 旋转x轴标签以便清晰显示
    plt.xticks(rotation=45)

    # 显示图表
    plt.show()

def ADF():
    adf_test = adfuller(temperature_data['AverageTemperature'], autolag='AIC')
    adf_result = {
        'ADF Statistic': adf_test[0],
        'p-value': adf_test[1],
        'Critical Values': adf_test[4]
    }