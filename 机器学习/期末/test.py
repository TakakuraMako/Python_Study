import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决图表中文
plt.rc('axes', unicode_minus=False)  # 解决 UserWarning: Glyph 8722 (\N{MINUS SIGN}) missing from current font.问题

def read_data_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    bus_data = {}
    current_bus = None
    header_skipped = False
    for line in lines:
        line = line.strip()
        if line.startswith('* 节点'):
            current_bus = line.split('"')[1].split()[0]
            bus_data[current_bus] = []
            header_skipped = False
        elif line.startswith('时间') or line.startswith('=========='):
            header_skipped = True
        elif line and current_bus and header_skipped:
            parts = line.split()
            if len(parts) == 3:
                try:
                    time, voltage, angle = parts
                    bus_data[current_bus].append((float(time), float(voltage), float(angle)))
                except ValueError:
                    continue
    
    # Convert to DataFrame
    dataframes = {}
    for bus, data in bus_data.items():
        df = pd.DataFrame(data, columns=['时间', '正序电压 (PU)', '正序角度 (度)'])
        dataframes[bus] = df
    
    return dataframes

# 使用示例
file_path = 'C:/Users/13619/Downloads/数据/故障线路：BUS-1~BUS-2-故障位置：10%.txt'
bus_dataframes = read_data_from_txt(file_path)

def visualize_bus_data(bus_dataframes, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for bus, df in bus_dataframes.items():
        plt.figure(figsize=(14, 6))
        
        # 电压随时间变化的折线图
        plt.subplot(1, 2, 1)
        sns.lineplot(x='时间', y='正序电压 (PU)', data=df)
        plt.title(f'{bus} 电压随时间变化')
        plt.xlabel('时间')
        plt.ylabel('正序电压 (PU)')
        
        # 角度随时间变化的折线图
        plt.subplot(1, 2, 2)
        sns.lineplot(x='时间', y='正序角度 (度)', data=df)
        plt.title(f'{bus} 角度随时间变化')
        plt.xlabel('时间')
        plt.ylabel('正序角度 (度)')
        
        plt.tight_layout()
        save_path = os.path.join(output_dir, f'{bus}_数据可视化.png')
        plt.savefig(save_path)
        plt.close()

# 可视化读取的结果
output_dir = 'C:/Users/13619/Downloads/数据/可视化结果'
visualize_bus_data(bus_dataframes, output_dir)
