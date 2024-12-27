import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller
# 使得图片正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('./时间序列分析/VAR/年度数据.xls')
df.set_index("年份", inplace=True)
df = df[::-1]  # 翻转数据，使年份递增

# # 可视化时间序列
# fig, axes = plt.subplots(nrows=3, ncols=2, dpi=120, figsize=(10, 8))
# for i, ax in enumerate(axes.flatten()):
#     col_name = df.columns[i]
#     ax.plot(df[col_name], color='blue', linewidth=1)
#     ax.set_title(col_name)
#     ax.xaxis.set_ticks_position('none')
#     ax.yaxis.set_ticks_position('none')
#     ax.spines["top"].set_alpha(0)
#     ax.tick_params(labelsize=6)

# plt.tight_layout()
# plt.show()

# # 格兰杰因果关系检验函数
# def grangers_causation_matrix(data, variables, maxlag=2, test='ssr_chi2test'):
#     """返回格兰杰因果关系的P值矩阵"""
#     df_result = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
#     for c in df_result.columns:
#         for r in df_result.index:
#             if r != c:  # 避免自检
#                 try:
#                     # 移除 verbose 参数，避免警告
#                     test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag)
#                     p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(maxlag)]
#                     min_p_value = np.min(p_values)
#                     df_result.loc[r, c] = min_p_value
#                 except ValueError as e:
#                     print(f"格兰杰检验失败: {r} -> {c}, 错误信息: {e}")
#                     df_result.loc[r, c] = np.nan
#     df_result.columns = [var + '_x' for var in variables]
#     df_result.index = [var + '_y' for var in variables]
#     return df_result

# # 执行格兰杰因果关系检验
# gc_matrix = grangers_causation_matrix(df, variables=df.columns, maxlag=2)
# print("格兰杰因果关系检验结果:")
# print(gc_matrix)

# # 可视化格兰杰因果关系检验结果
# plt.figure(figsize=(10, 8))
# sns.heatmap(gc_matrix, annot=True, cmap="coolwarm", cbar=True)
# plt.title("格兰杰因果关系检验 (P 值矩阵)")
# plt.tight_layout()
# plt.show()

# 将数据集拆分为训练集和测试集
nobs = 4  # 选择最后4个观测值作为测试集
df_train, df_test = df[0:-nobs], df[-nobs:]

# 检查数据集大小
print(f"训练集大小: {df_train.shape}")
print(f"测试集大小: {df_test.shape}")

# ADF
def adfuller_test(series, signif=0.05, name=''):
    """对给定时间序列进行ADF测试并打印报告"""
    r = adfuller(series, autolag='AIC')
    output = {
        'Test Statistic': round(r[0], 4),
        'p-value': round(r[1], 4),
        'Lags Used': r[2],
        'Number of Observations Used': r[3],
    }
    print(f'对 "{name}" 的ADF检验')
    print(f"检验统计量: {output['Test Statistic']}")
    print(f"p值: {output['p-value']}")
    print(f"使用的滞后阶数: {output['Lags Used']}")
    print(f"使用的样本数量: {output['Number of Observations Used']}")
    print("临界值:")
    for key, value in r[4].items():
        print(f"    {key}: {round(value, 4)}")
    if r[1] <= signif:
        print("=> 拒绝原假设：序列是平稳的。\n")
    else:
        print("=> 无法拒绝原假设：序列是非平稳的。\n")

# # 对训练集的每个列变量进行ADF测试
# print("原始数据ADF测试结果：")
# for name, column in df_train.items():  # 修复 iteritems 改为 items
#     adfuller_test(column, name=name)

# # 进行一次差分
# df_differenced = df_train.diff().dropna()

# # 对差分后的数据进行ADF测试
# print("一阶差分数据ADF测试结果：")
# for name, column in df_differenced.items():
#     adfuller_test(column, name=name)

# # 如果仍不平稳，进行二阶差分
# df_differenced_2 = df_differenced.diff().dropna()
# print("二阶差分数据ADF测试结果：")
# for name, column in df_differenced_2.items():
#     adfuller_test(column, name=name)

# 对数变换
df_log = np.log(df)
print("对数变换后的原始数据ADF测试结果：")
for name, column in df_log.items():
    adfuller_test(column, name=name)

# 对数变换后进行一次差分
df_log_diff = df_log.diff().dropna()

# 对差分后的数据进行 ADF 测试
print("对数变换后的一阶差分数据ADF测试结果：")
for name, column in df_log_diff.items():
    adfuller_test(column, name=name)

# 如果仍不平稳，可以进行二阶差分
df_log_diff_2 = df_log_diff.diff().dropna()
print("对数变换后的二阶差分数据ADF测试结果：")
for name, column in df_log_diff_2.items():
    adfuller_test(column, name=name)

# 最终平稳化的数据
df_train_final = df_log_diff_2
print("最终训练数据（对数变换后差分处理）：")
print(df_train_final.head())