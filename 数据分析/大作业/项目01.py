import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def visualize(df):
    # SEX
    counts_sex = df['SEX'].value_counts().sort_index()
    plt.figure()
    counts_sex.plot(kind='pie', autopct='%1.1f%%')
    plt.title('SEX 分布（饼图）')
    plt.ylabel('')
    plt.show()

    # EDUCATION
    counts_edu = df['EDUCATION'].value_counts().sort_index()
    plt.figure()
    counts_edu.plot(kind='bar')
    plt.title('EDUCATION 分布（柱状图）')
    plt.xlabel('Education Category')
    plt.ylabel('Count')
    plt.show()

    # MARRIAGE
    counts_mar = df['MARRIAGE'].value_counts().sort_index()
    plt.figure()
    counts_mar.plot(kind='pie', autopct='%1.1f%%')
    plt.title('MARRIAGE 分布（饼图）')
    plt.ylabel('')
    plt.show()

    # AGE
    plt.figure()
    df['AGE'].hist(bins=20)
    plt.title('AGE 分布直方图')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.show()

    # 可视化清洗后 PAY_0 分布直方图
    plt.figure()
    df['PAY_0'].hist(bins=10)
    plt.title('清洗后 PAY_0 分布直方图')
    plt.xlabel('PAY_0 (0=on time, >0 delay months)')
    plt.ylabel('Count')
    plt.show()

# 读取数据
df = pd.read_excel('./数据分析/大作业/default of credit card clients.xlsx', header=1)
print(df.shape)  # 输出数据的行列数
# 清洗 EDUCATION 和 MARRIAGE
df['EDUCATION'] = df['EDUCATION'].replace({5: 4, 6: 4})
df['MARRIAGE'] = df['MARRIAGE'].apply(lambda x: x if x in [1, 2, 3] else 3)
# 清洗前 PAY_0 分布
print("清洗前 PAY_0 分布：")
print(df['PAY_0'].value_counts().sort_index())

# PAY 列名列表
pay_cols = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']

# 将所有 <= 0 的值映射为 0 （按字典：-1 表示正常还款，0 也视为无逾期）
df[pay_cols] = df[pay_cols].clip(lower=0)

# 清洗后 PAY_0 分布
print("\n清洗后 PAY_0 分布：")
print(df['PAY_0'].value_counts().sort_index())

# visualize(df)

df.to_excel('./数据分析/大作业/清洗后数据.xlsx', index=False)