import pandas as pd
import glob
import os

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

# 定义文件夹路径
folder_path = './机器学习/用户用电数据'

# 获取所有CSV文件的文件路径
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# 初始化空的DataFrame列表
data_list = []

# 读取每个CSV文件并添加到列表中
for file in csv_files:
    data = pd.read_csv(file, header=None, names=['date', 'value'])
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data['month_day'] = data['date'].dt.strftime('%m%d')
    data_list.append(data)

# 将所有DataFrame合并为一个
all_data = pd.concat(data_list, ignore_index=True)

# 计算每日的峰值、平均值、谷值和谷峰差
daily_stats = all_data.groupby('month_day')['value'].agg(
    peak_value='max',
    average_value='mean',
    trough_value='min'
).reset_index()

# 计算谷峰差
daily_stats['peak_trough_diff'] = daily_stats['peak_value'] - daily_stats['trough_value']

# 显示结果
print(daily_stats)

# 保存每日统计值到新CSV文件
daily_stats.to_csv('./daily_stats.csv', index=False)
