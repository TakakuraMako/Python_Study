import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 设置随机种子以保证可重复性
np.random.seed(42)

# 生成MA(2)模型的随机噪声
n = 10000  # 时间序列长度
theta = [0.4, -0.5]  # MA参数
white_noise = np.random.normal(size=n)

# 生成MA(2)时间序列
ma_series = np.zeros(n)
for t in range(2, n):
    ma_series[t] = white_noise[t] + theta[0] * white_noise[t-1] + theta[1] * white_noise[t-2]

# 绘制MA(2)时间序列
plt.figure(figsize=(12, 6))
plt.plot(ma_series, label='MA(2) Time Series', color='blue')
plt.title('MA(2) Time Series')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()

# 计算并绘制自相关函数（ACF）和偏自相关函数（PACF）
fig, ax = plt.subplots(2, 1, figsize=(12, 10))

# 自相关函数
sm.graphics.tsa.plot_acf(ma_series, lags=20, ax=ax[0])
ax[0].set_title('Autocorrelation Function (ACF)')

# 偏自相关函数
sm.graphics.tsa.plot_pacf(ma_series, lags=20, ax=ax[1])
ax[1].set_title('Partial Autocorrelation Function (PACF)')

plt.tight_layout()
plt.show()
