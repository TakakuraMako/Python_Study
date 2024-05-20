import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import glob
import os
import re
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
    data_new = data.groupby('Day')['Aggregate'].sum().reset_index()
    return data, data_new

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

'''
for i in range(len(csv_files)):
    data = pd.read_csv(csv_files[i])
    data, data_new = Data_preprocessing(data)
    _add = re.search(r"House\d+", csv_files[i].replace('_','')).group()
    data_day = pd.merge(data_day, data_new, how='outer', on='Day',suffixes=['',_add])
data_day['Day'] = data_day['Day'].astype(str)
print(data_day.dtypes)
data_day.to_csv('./机器学习/data_day.csv',index=False)
'''
data_day = pd.read_csv('./机器学习/data_day.csv',converters={u'Day':str})
print(data_day['Day'])
Data_Visualize(data_day)



'''

# 标准化数据
scaler = StandardScaler()
data['Aggregate_scaled'] = scaler.fit_transform(data[['Aggregate']])

# 使用KMeans进行聚类
kmeans = KMeans(n_clusters=3, random_state=42)
data['cluster'] = kmeans.fit_predict(data[['Aggregate_scaled']])

# 可视化聚类结果
plt.figure(figsize=(12, 6))
plt.scatter(pd.to_datetime(data['Unix']), data['Aggregate'], c=data['cluster'], cmap='viridis')
plt.title('House Electricity Usage Clustering')
for i in range(2):
    data = pd.read_csv(csv_files[i])
    data, data_new = Data_preprocessing(data)
    data_list.append(data_new)
Data_Visualize(data_list)



'''
'''
# 标准化数据
scaler = StandardScaler()
data['Aggregate_scaled'] = scaler.fit_transform(data[['Aggregate']])

# 使用KMeans进行聚类
kmeans = KMeans(n_clusters=3, random_state=42)
data['cluster'] = kmeans.fit_predict(data[['Aggregate_scaled']])

# 可视化聚类结果
plt.figure(figsize=(12, 6))
plt.scatter(pd.to_datetime(data['Unix']), data['Aggregate'], c=data['cluster'], cmap='viridis')
plt.title('House Electricity Usage Clustering')
plt.xlabel('Time')
plt.ylabel('Electricity Usage')
plt.grid(True)
plt.ylabel('Electricity Usage')
plt.grid(True)
plt.show()
'''
