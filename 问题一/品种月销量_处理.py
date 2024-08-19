import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False

file_path_weekly = './问题一/单品日销量处理.xlsx'

# 从Excel文件中读取数据
df_weekly = pd.read_excel(file_path_weekly)
# 将周的计算方式改为从数据的最早时间开始计算的第几周

# 找到数据中的最早日期
earliest_date = df_weekly['销售日期'].min()

# 计算每个日期相对于最早日期的第几周
df_weekly['周数'] = ((df_weekly['销售日期'] - earliest_date).dt.days // 7) + 1

# 按品类名称和自定义的周数进行分组，并计算每周的总销量
df_weekly_grouped_custom = df_weekly.groupby(['品类名称', '周数'])['销量(千克)'].sum().reset_index()

# 绘制每个品类每周销量的折线图
plt.figure(figsize=(14, 8))
for category in df_weekly_grouped_custom['品类名称'].unique():
    category_data = df_weekly_grouped_custom[df_weekly_grouped_custom['品类名称'] == category]
    plt.plot(category_data['周数'], category_data['销量(千克)'], label=category)

# 设置图表标题和标签
plt.title('品类每周销量折线图')
plt.xlabel('周')
plt.ylabel('销量(千克)')
plt.legend(title='品类名称', bbox_to_anchor=(1.05, 1), loc='upper left')

# 自动调整布局，确保标签不重叠
plt.xticks(rotation=45)
plt.tight_layout()

# 显示图表
plt.show()
