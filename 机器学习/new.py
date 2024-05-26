import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import glob
import os
import re
import matplotlib

matplotlib.rc("font", family='MicroSoft YaHei', weight="bold")

def Data_preprocessing(data):
    # 和时间有关，向前填充
    data = data.ffill()
    data = data.bfill()

    # 转化为pandas时间格式
    data['Time'] = pd.to_datetime(data['Time'], format='%Y/%m/%d %H:%M')
    data['Day'] = data['Time'].dt.strftime('%m%d')

    # 首尾记录不是完整一天，去除
    data = data.drop(data[data['Day'] == data.iloc[0, -1]].index).reset_index(drop=True)
    data = data.drop(data[data['Day'] == data.iloc[-1, -1]].index).reset_index(drop=True)

    return data

def Max_hour(data):
    # 提取日期和小时
    data['hour'] = data['Time'].dt.hour

    # 按小时分组并计算每小时的总用电量
    hourly_sum = data.groupby('hour')['Aggregate'].sum().reset_index()

    # 找出最大负荷时间
    max_load_hour = hourly_sum.loc[hourly_sum['Aggregate'].idxmax()]

    # 结果
    max_hour = max_load_hour['hour']
    max_value = max_load_hour['Aggregate']
    return max_hour, max_value

def Data_Visualize(data_day):
    # 每天用电
    plt.figure()
    y = []
    x = data_day['Day'].tolist()
    print(x)
    for i in range(len(csv_files)):
        y = data_day.iloc[:, i + 1]
        plt.plot(x, y)
    plt.xlabel('Time')
    plt.ylabel('Aggregate')
    plt.xticks(range(0, len(x), 5), rotation=45)
    plt.grid(axis='y')
    plt.show()

# 主代码块
folder_path = './机器学习/用户用电数据'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
data_list = []
data_day = pd.DataFrame({'Day': []})

index = ['日峰值', '日谷值', '日均值', '谷峰差', '最高用电时段', '日峰谷差率']
data_new = pd.DataFrame({}, index=index)

for i in range(len(csv_files)):
    data = pd.read_csv(csv_files[i])
    data = Data_preprocessing(data)
    _add = re.search(r"House\d+", csv_files[i].replace('_', '')).group()
    data_new.loc['日均值', _add] = data['Aggregate'].mean()
    data_new.loc['日峰值', _add] = data['Aggregate'].max()
    data_new.loc['日谷值', _add] = data['Aggregate'].min()
    data_new.loc['谷峰差', _add] = data_new.loc['日峰值', _add] - data_new.loc['日谷值', _add]
    data_new.loc['日峰谷差率', _add] = data_new.loc['日谷值', _add] / data_new.loc['日峰值', _add]
    max_hour, _ = Max_hour(data)
    data_new.loc['最高用电时段', _add] = max_hour
print(data_new)

fig, axs = plt.subplots(len(index), 1, figsize=(50, 30))
#fig.subplots_adjust(wspace=0.3, hspace=0.3, bottom=0.1, top=0.2)
#fig = plt.figure(dpi=200)
# 生成每个列的柱状图
for i in range(len(index)):
    axs[i].plot(data_new.iloc[i], marker='o')
    axs[i].set_title(index[i])
    axs[i].set_ylabel('Value')
    axs[i].grid(True)

# 调整布局
fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.5)
#plt.tight_layout(h_pad=50)
plt.show()

# 标准化数据
scaler = StandardScaler()
data_new = data_new.T
data_scaled = scaler.fit_transform(data_new)

# 选择聚类算法（K-means）
kmeans = KMeans(n_clusters=4, random_state=0)
data_new['cluster'] = kmeans.fit_predict(data_scaled)

# 聚类结果可视化，选择最高用电时段和日均值作为坐标轴
x_axis = '最高用电时段'
y_axis = '日均值'
x_index = index.index(x_axis)
y_index = index.index(y_axis)

plt.figure(figsize=(10, 6))
plt.scatter(data_scaled[:, x_index], data_scaled[:, y_index], c=data_new['cluster'], cmap='viridis', marker='o')

for i, txt in enumerate(data_new.index):
    plt.annotate(txt, (data_scaled[i, x_index], data_scaled[i, y_index]))

plt.xlabel(f'Scaled {x_axis}')
plt.ylabel(f'Scaled {y_axis}')
plt.title('Cluster Analysis of House Electricity Usage')
plt.show()

# 打印聚类结果
print(data_new)
