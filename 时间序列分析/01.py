import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 数据读取和处理
file_path = './时间序列分析/weather北京.csv'
df = pd.read_csv(file_path, encoding='gbk')
df['最高温'] = df['最高温'].str.replace('°', '').astype(int)
df['最低温'] = df['最低温'].str.replace('°', '').astype(int)
df['日期'] = pd.to_datetime(df['日期'].str.strip())
df.set_index('日期', inplace=True)

# 计算平均温度
df['平均温'] = (df['最高温'] + df['最低温']) / 2
temp_data = df[['平均温']]

# 绘制原始数据的 ACF 和 PACF 图
plt.figure(figsize=(12, 6))

# ACF 图
plt.subplot(121)
plot_acf(temp_data, ax=plt.gca(), lags=20)
plt.title('ACF of Original Data')

# PACF 图
plt.subplot(122)
plot_pacf(temp_data, ax=plt.gca(), lags=20)
plt.title('PACF of Original Data')

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
plt.title(f'Differenced ACF (d={d_value})')

# PACF 图（差分后的数据）
plt.subplot(122)
plot_pacf(diff_temp, ax=plt.gca(), lags=20)
plt.title(f'Differenced PACF (d={d_value})')

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
plt.plot(temp_data.index, temp_data['平均温'], label='Observed Avg Temp')
forecast_dates = pd.date_range(temp_data.index[-1] + pd.Timedelta(days=1), periods=10)
plt.plot(forecast_dates, forecast_mean, label='Predicted Avg Temp (ARIMA)', linestyle='--', color='red')
plt.fill_between(forecast_dates, forecast_conf_int.iloc[:, 0], forecast_conf_int.iloc[:, 1], color='red', alpha=0.3)
plt.title(f'Average Temperature Forecast using ARIMA {auto_model.order}')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.show()
