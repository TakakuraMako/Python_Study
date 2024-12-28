import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller
import seaborn as sns
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR
from statsmodels.stats.stattools import durbin_watson
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 数据导入和预处理
df = pd.read_csv('./时间序列分析/VAR/data.csv')  # 读取数据
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)  # 将日期设为索引

fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(10,6))
for i, ax in enumerate(axes.flatten()):
    data = df[df.columns[i]]
    ax.plot(data, color='red', linewidth=1)
    ax.set_title(df.columns[i])
plt.tight_layout()
plt.show()


# 计算相关性矩阵
correlation_matrix = df.corr()

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("变量之间的相关性热力图", fontsize=16)
plt.show()

df_numeric = df.select_dtypes(include=['float64', 'int64'])  # 确保数据中只有数值列

# 定义格兰杰因果关系矩阵函数
def grangers_causation_matrix(data, variables, maxlag=12, test='ssr_chi2test', verbose=False):
    # 创建一个空的 DataFrame 用于存储结果
    df_result = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    
    # 遍历变量，逐一进行格兰杰因果关系检验
    for c in df_result.columns:
        for r in df_result.index:
            # 对每对变量进行检验
            try:
                test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
                p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]  # 提取每个滞后阶数的 p 值
                min_p_value = np.min(p_values)  # 选择最小的 p 值
                df_result.loc[r, c] = min_p_value
            except Exception as e:
                # 如果检验失败，标记为 NaN
                df_result.loc[r, c] = np.nan

    # 重命名行和列
    df_result.columns = [var + '_x' for var in variables]
    df_result.index = [var + '_y' for var in variables]
    return df_result

# 调用函数并生成结果
granger_matrix = grangers_causation_matrix(df_numeric, variables=df.columns, maxlag=12, test='ssr_chi2test', verbose=False)
# 打印格兰杰因果关系矩阵结果
print("格兰杰因果关系矩阵:")
print(granger_matrix)
# 绘制格兰杰因果关系矩阵的热力图
plt.figure(figsize=(10, 8))
sns.heatmap(granger_matrix.astype(float), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("格兰杰因果关系矩阵热力图", fontsize=16)
plt.xlabel("预测变量 (X)", fontsize=12)
plt.ylabel("响应变量 (Y)", fontsize=12)
plt.tight_layout()
plt.show()

# 定义ADF检验函数
def adfuller_test(series, signif=0.05, name=''):
    """
    Perform Augmented Dickey-Fuller test and print results.
    """
    r = adfuller(series.dropna(), autolag='AIC')  # 去除空值以确保ADF检验的正确性
    output = {
        'test_statistic': round(r[0], 4),
        'pvalue': round(r[1], 4),
        'n_lags': round(r[2], 4),
        'n_obs': r[3]
    }
    p_value = output['pvalue']

    # 打印ADF检验的结果
    print(f'ADF检验: "{name}"')
    print('-' * 40)
    print(f'零假设: 数据存在单位根，非平稳')
    print(f'显著性水平: {signif}')
    print(f'检验统计量: {output["test_statistic"]}')
    print(f'滞后阶数: {output["n_lags"]}')
    print(f'样本数: {output["n_obs"]}')
    for key, val in r[4].items():
        print(f'临界值 {key}: {round(val, 3)}')

    if p_value <= signif:
        print(f'P值 = {p_value}，拒绝零假设。数据是平稳的。')
    else:
        print(f'P值 = {p_value}，不能拒绝零假设。数据是非平稳的。')
    print('\n')

# 对数据集中的每列进行ADF检验
for name, column in df.items():  
    adfuller_test(column, name=name)

# 划分训练集和测试集
nobs = 4  # 最后四个时间点作为测试集
df_train, df_test = df_numeric[0:-nobs], df_numeric[-nobs:]

# 创建一个列表来存储所有ADF检验的结果
adf_results = []

# 一阶差分ADF检验结果
df_differenced = df_train.diff().dropna()
for name, column in df_differenced.items():
    r = adfuller(column.dropna(), autolag='AIC')
    adf_results.append({
        "Variable": name,
        "Difference": "1st",
        "Test Statistic": round(r[0], 4),
        "P-Value": round(r[1], 4),
        "Lags Used": round(r[2], 4),
        "N Observations": r[3],
        "Significant": r[1] < 0.05
    })

# 二阶差分ADF检验结果
df_differenced = df_differenced.diff().dropna()
for name, column in df_differenced.items():
    r = adfuller(column.dropna(), autolag='AIC')
    adf_results.append({
        "Variable": name,
        "Difference": "2nd",
        "Test Statistic": round(r[0], 4),
        "P-Value": round(r[1], 4),
        "Lags Used": round(r[2], 4),
        "N Observations": r[3],
        "Significant": r[1] < 0.05
    })

# 将结果转换为DataFrame
adf_results_df = pd.DataFrame(adf_results)

# 保存结果为文件
output_file = './时间序列分析/VAR/adf_results.csv'
adf_results_df.to_csv(output_file, index=False)

# 创建VAR模型
model = VAR(df_differenced)
# 选择 lag=4 拟合 VAR 模型
model_fitted = model.fit(4)

# 输出模型摘要
print(model_fitted.summary())

coefficients = model_fitted.params

# 将系数矩阵保存为 CSV 文件
var_coefficients_file = './时间序列分析/VAR/var_model_coefficients.csv'
coefficients.to_csv(var_coefficients_file)



# Durbin-Watson 检验，检查残差的相关性
dw_test = durbin_watson(model_fitted.resid)

# 创建一个结果字典，用于保存 Durbin-Watson 检验结果
dw_results = {
    "Variable": [],
    "Durbin-Watson Statistic": []
}

# 将 Durbin-Watson 检验结果存入字典
for col, val in zip(df_differenced.columns, dw_test):
    dw_results["Variable"].append(col)
    dw_results["Durbin-Watson Statistic"].append(round(val, 2))

# 转换为 DataFrame
dw_results_df = pd.DataFrame(dw_results)

# 保存为文件
output_file = './时间序列分析/VAR/durbin_watson_results.csv'
dw_results_df.to_csv(output_file, index=False)


# 确定滞后阶数
lag_order = model_fitted.k_ar

# 获取用于预测的输入数据
forecast_input = df_differenced.values[-lag_order:]

# 进行预测，预测步数为测试集大小 (nobs)
fc = model_fitted.forecast(y=forecast_input, steps=nobs)

# 将预测结果转换为 DataFrame
df_forecast = pd.DataFrame(fc, index=df.index[-nobs:], columns=df_differenced.columns + '_2d')

# 保存预测结果为 CSV 文件
forecast_file = './时间序列分析/VAR/var_model_forecast.csv'
# df_forecast.to_csv(forecast_file)

# 定义函数将差分后的值还原为原始数据
def invert_transformation(df_train, df_forecast):
    """
    Invert the differencing transformation to restore the forecast to the original scale.
    """
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:
        # 还原一阶差分
        df_fc[str(col) + '_1d'] = (df_train[col].iloc[-1] - df_train[col].iloc[-2]) + df_fc[str(col) + '_2d'].cumsum()
        # 还原到原始数据
        df_fc[str(col) + '_forecast'] = df_train[col].iloc[-1] + df_fc[str(col) + '_1d'].cumsum()
    return df_fc

# 还原预测值到原始数据
df_results = invert_transformation(df_train, df_forecast)

# 保存预测结果为文件
forecast_file = './时间序列分析/VAR/var_model_forecast_restored.csv'
df_results.to_csv(forecast_file)
print(f"预测结果已保存到文件：{forecast_file}")

# 选择需要比较的列
columns_to_plot = df_numeric.columns

# 创建可视化
# 创建可视化，修改布局防止标题和坐标重叠
fig, axes = plt.subplots(nrows=int(len(columns_to_plot) / 2), ncols=2, dpi=150)
for i, (col, ax) in enumerate(zip(columns_to_plot, axes.flatten())):
    df_results[col + '_forecast'].plot(legend=True, ax=ax, label="预测值").autoscale(axis='x', tight=True)
    df_test[col].plot(legend=True, ax=ax, label="实际值")
    ax.set_title(col + ": 预测值 vs 实际值", fontsize=10, pad=10)  # 增加 pad 参数防止标题与图表重叠
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.spines["top"].set_alpha(0)
    ax.tick_params(labelsize=8)

# 调整子图之间的间距
plt.tight_layout(h_pad=2, w_pad=2)  # 调整子图的垂直和水平间距
plt.show()
