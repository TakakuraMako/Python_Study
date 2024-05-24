import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import glob
import os
import re
import matplotlib

matplotlib.rc("font",family='MicroSoft YaHei',weight="bold")
def Data_preprocessing(data):
        #和时间有关，向前填充
    data = data.ffill()
    data = data.bfill()

    #转化为pandas时间格式
    data['Time'] = pd.to_datetime(data['Time'], format='%Y/%m/%d %M:%S')
    #data = data.iloc[0:100000]
    data['Day'] = data['Time'].dt.strftime('%m%d')

    #首尾记录不是完整一天，去除
    data = data.drop(data[data['Day'] == data.iloc[0,-1]].index).reset_index()
    data = data.drop(data[data['Day'] == data.iloc[-1,-1]].index).reset_index()


    return data

def Max_hour(data):
    # 提取日期和小时
    data['hour'] = data['Time'].dt.strftime('%H')

    # 按小时分组并计算每小时的总用电量
    hourly_sum = data.groupby('hour')['Aggregate'].sum().reset_index()

    # 找出最大负荷时间
    max_load_hour = hourly_sum.loc[hourly_sum['Aggregate'].idxmax()]

    # 结果
    max_hour = max_load_hour['hour']
    max_value = max_load_hour['Aggregate']
    return max_hour

def Data_Visualize(data_day):
    #每天用电
    plt.figure()
    y = []
    x = data_day['Day'].tolist()
    print(x)
    #x = np.linspace(0,data_new.shape[0],data_new.shape[0])
    for i in range(len(csv_files)):
        y = data_day.iloc[:,i+1]
        plt.plot(x,y)
    plt.xlabel('Time')
    plt.ylabel('Aggregate')
    plt.xticks(range(0,len(x),5),rotation = 45)
    #plt.yticks(range(1,100,2),rotation = 45)
    #plt.xticks(rotation = 45)
    plt.grid(axis = 'y')
    plt.show()



folder_path = './机器学习/用户用电数据'
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
data_list = []
data_day = pd.DataFrame({
    'Day':[]
})
#查看基本信息
'''
print(data.head)
print(data.info())
print(data.shape)
print(data.describe())
'''
index = ['日峰值','日谷值', '日均值', '谷峰差', '最高用电时段','日峰谷差率']
data_new = pd.DataFrame({},index = index)
for i in range(2):
    data = pd.read_csv(csv_files[i])
    data = Data_preprocessing(data)
    _add = re.search(r"House\d+", csv_files[i].replace('_','')).group()
    data_new.loc['日均值',_add] = data['Aggregate'].mean()
    data_new.loc['日峰值',_add] = data['Aggregate'].max()
    data_new.loc['日谷值',_add] = data['Aggregate'].min()
    data_new.loc['谷峰差',_add] = data_new.loc['日峰值',_add]-data_new.loc['日谷值',_add]
    data_new.loc['日峰谷差率',_add] = data_new.loc['日谷值',_add]/data_new.loc['日峰值',_add]
    data_new.loc['最高用电时段',_add] = Max_hour(data)
print(data_new)


fig, axs = plt.subplots(len(index), 1, figsize=(20, 20))

# 生成每个列的柱状图
for i in range(len(index)):
    axs[i].plot(data_new.iloc[i], marker='o')
    axs[i].set_title(index[i])
    axs[i].set_ylabel('Value')
    axs[i].grid(True)

# 调整布局
plt.tight_layout()
plt.show()



# 标准化数据
scaler = StandardScaler()
data_new = data_new.T
data_scaled = scaler.fit_transform(data_new)

# 选择聚类算法（K-means）
kmeans = KMeans(n_clusters=4, random_state=0)
data_new['cluster'] = kmeans.fit_predict(data_scaled)

# 聚类结果可视化
plt.figure(figsize=(10, 6))
plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=data_new['cluster'], cmap='viridis', marker='o')

for i, txt in enumerate(data_new.index):
    plt.annotate(txt, (data_scaled[i, 0], data_scaled[i, 1]))

'''
plt.xlabel('Scaled Peak Value')
plt.ylabel('Scaled Average Value')
plt.title('Cluster Analysis of House Electricity Usage')
#plt.colorbar(label='Cluster')
'''
plt.show()

# 打印聚类结果
print(data_new)