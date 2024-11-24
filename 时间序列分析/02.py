import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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

def ADF(series):
    result = adfuller(series)
    output = {
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Used Lag": result[2],
        "Number of Observations": result[3],
        "Critical Values": result[4]
    }
    return output

def acf_pacf(data):
    # Plotting ACF and PACF for the 'AverageTemperature' series
    plt.figure(figsize=(12, 6))

    # ACF plot
    plt.subplot(1, 2, 1)
    plot_acf(data['AverageTemperature'], lags=40, ax=plt.gca())
    plt.title('ACF')

    # PACF plot
    plt.subplot(1, 2, 2)
    plot_pacf(data['AverageTemperature'], lags=40, ax=plt.gca())
    plt.title('PACF')

    plt.tight_layout()
    plt.show()

def season_diff(data):
    # 季节性差分，假设周期为12
    seasonal_diff = data['AverageTemperature'].diff(12)
    data['AverageTemperature'] = seasonal_diff
    # 去除缺失值（由于差分会在开头产生 NaN 值）
    seasonal_diff = seasonal_diff.dropna()

    # 绘制季节性差分后的 ACF 和 PACF
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plot_acf(seasonal_diff, lags=40, ax=plt.gca())
    plt.title('ACF')

    plt.subplot(1, 2, 2)
    plot_pacf(seasonal_diff, lags=40, ax=plt.gca())
    plt.title('PACF')

    plt.tight_layout()
    plt.show()
    return data

def diff(data):
    # 对 'AverageTemperature' 数据进行一次差分
    data_diff = data['AverageTemperature'].diff().dropna()
    data['AverageTemperature'] = data_diff
    # 绘制差分后的数据
    plt.figure(figsize=(12, 6))
    plt.plot(data_diff, color='orange')
    plt.title('差分后数据')
    plt.xlabel('时间')
    plt.ylabel('差分后温度')
    plt.show()
    return data


def canchafenxi(data):
    data = data.asfreq('MS')
    model = SARIMAX(data['AverageTemperature'],
                    order=(4, 2, 4),                # 非季节性部分
                    seasonal_order=(1, 1, 1, 12)    # 季节性部分
                )
    data = data.asfreq('MS') 
    # 拟合SARIMA模型
    sarima_fit = model.fit(disp=False)

    # 提取残差
    residuals = sarima_fit.resid

    # 残差的 ACF 图
    plt.figure(figsize=(12, 6))
    plot_acf(residuals, lags=40, ax=plt.gca())
    plt.title('残差ACF')
    plt.show()

    # 绘制残差的时间序列图
    plt.figure(figsize=(12, 6))
    plt.plot(residuals)
    plt.title('Residuals Time Series')
    plt.xlabel('Time')
    plt.ylabel('残差数据')
    plt.show()

    # Ljung-Box 检验，用于检验残差的独立性
    ljung_box_results = acorr_ljungbox(residuals, lags=[10], return_df=True)
    print("Ljung-Box Test for Residuals:")
    print(ljung_box_results)

    # 对原数据进行白噪声检验（Ljung-Box检验）
    ljung_box_results_original = acorr_ljungbox(data['AverageTemperature'].dropna(), lags=[10], return_df=True)
    print("Ljung-Box Test for Original Data:")
    print(ljung_box_results_original)

def forecast(data):
    # 定义并拟合 SARIMA(4,2,4)(1,1,1,12) 模型
    model = SARIMAX(data['AverageTemperature'],
                    order=(4, 2, 4),
                    seasonal_order=(1, 1, 1, 12))

    # 拟合模型
    sarima_fit = model.fit(disp=False)

    # 进行预测
    forecast_steps = 12  # 预测未来12个月的数据
    forecast = sarima_fit.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(data.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq='MS')
    forecast_series = forecast.predicted_mean
    forecast_series.index = forecast_index

    # 绘制预测结果
    plt.figure(figsize=(12, 6))
    plt.plot(data['AverageTemperature'], label='历史数据')
    plt.plot(forecast_series, color='orange', label='预测数据')
    plt.fill_between(forecast_index, forecast.conf_int().iloc[:, 0], forecast.conf_int().iloc[:, 1], color='orange', alpha=0.2)
    plt.title('预测')
    plt.xlabel('日期')
    plt.ylabel('温度')
    plt.legend()
    plt.show()
    # 获取预测的具体数据，包括预测值和置信区间
    forecast_data = forecast.predicted_mean.to_frame(name='Forecast')
    forecast_data['Lower CI'] = forecast.conf_int().iloc[:, 0]
    forecast_data['Upper CI'] = forecast.conf_int().iloc[:, 1]
    evaluate_model(data, forecast_series)

def evaluate_model(data, forecast_series):
    # 为模型评价准备实际值和预测值
    # 使用历史数据的最后12个月作为实际值
    actual_values = data['AverageTemperature'][-12:]
    predicted_values = forecast_series[:len(actual_values)]

    # 计算 MSE, MAE, 和 R2-score
    mse = mean_squared_error(actual_values, predicted_values)
    mae = mean_absolute_error(actual_values, predicted_values)
    r2 = r2_score(actual_values, predicted_values)

    # 输出评价指标
    print("模型评价指标：")
    print(f"MSE: {mse}")
    print(f"MAE: {mae}")
    print(f"R2-score: {r2}")
forecast(temperature_data)