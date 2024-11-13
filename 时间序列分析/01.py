import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimSun']  # 宋体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 数据读取和处理
file_path = './时间序列分析/data.csv'
df = pd.read_csv(file_path, encoding='gbk')
df['日期'] = pd.to_datetime(df['日期'].str.strip())
df.set_index('日期', inplace=True)

temp_data = df[['平均温度']]

# 绘制原始数据的 ACF 和 PACF 图
plt.figure(figsize=(12, 6))

# ACF 图
plt.subplot(121)
plot_acf(temp_data, ax=plt.gca(), lags=20)
plt.title('原始数据的自相关图 (ACF)', fontsize=12)
plt.xlabel('滞后期', fontsize=12)
plt.ylabel('自相关系数', fontsize=12)

# PACF 图
plt.subplot(122)
plot_pacf(temp_data, ax=plt.gca(), lags=20)
plt.title('原始数据的偏自相关图 (PACF)', fontsize=12)
plt.xlabel('滞后期', fontsize=12)
plt.ylabel('偏自相关系数', fontsize=12)

plt.tight_layout()
plt.show()

# 自动选择 ARIMA 模型的参数 (p, d, q)
auto_model = auto_arima(temp_data, start_p=1, start_q=1, max_p=5, max_q=5, seasonal=False, 
                        stepwise=True, trace=True, error_action='ignore', suppress_warnings=True)

# 输出选择的最佳参数
print(f"最佳 ARIMA 模型参数 (p, d, q): {auto_model.order}")

# 使用自动选择的 ARIMA 模型进行拟合
model = ARIMA(temp_data, order=auto_model.order)
result = model.fit()

# 打印模型摘要
print(result.summary())

# 进行差分处理（根据自动选择的 d 值进行差分）
d_value = auto_model.order[1]  # d 值，自动选择的差分阶数
diff_temp = temp_data.diff(d_value).dropna()

# 绘制差分后的 ACF 和 PACF 图
plt.figure(figsize=(12, 6))

# ACF 图（差分后的数据）
plt.subplot(121)
plot_acf(diff_temp, ax=plt.gca(), lags=20)
plt.title(f'差分后的自相关图 (d={d_value})', fontsize=12)
plt.xlabel('滞后期', fontsize=12)
plt.ylabel('自相关系数', fontsize=12)

# PACF 图（差分后的数据）
plt.subplot(122)
plot_pacf(diff_temp, ax=plt.gca(), lags=20)
plt.title(f'差分后的偏自相关图 (d={d_value})', fontsize=12)
plt.xlabel('滞后期', fontsize=12)
plt.ylabel('偏自相关系数', fontsize=12)

plt.tight_layout()
plt.show()

# 预测未来 10 天的平均温度
forecast = result.get_forecast(steps=10)
forecast_mean = forecast.predicted_mean
forecast_conf_int = forecast.conf_int()

# 打印预测结果
print("未来10天的平均温度预测：")
print(forecast_mean)

# 可视化预测结果
plt.figure(figsize=(10, 6))
plt.plot(temp_data.index, temp_data['平均温'], label='实际观测平均温度')
forecast_dates = pd.date_range(temp_data.index[-1] + pd.Timedelta(days=1), periods=10)
plt.plot(forecast_dates, forecast_mean, label='预测平均温度 (ARIMA)', linestyle='--', color='red')
plt.fill_between(forecast_dates, forecast_conf_int.iloc[:, 0], forecast_conf_int.iloc[:, 1], color='red', alpha=0.3)
plt.title(f'基于 ARIMA{auto_model.order} 模型的平均温度预测', fontsize=12)
plt.xlabel('日期', fontsize=12)
plt.ylabel('温度 (°C)', fontsize=12)
plt.legend()
plt.show()
