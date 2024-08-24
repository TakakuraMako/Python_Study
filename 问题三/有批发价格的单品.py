import pandas as pd

# 加载Excel文件
file_path = './附件3.xlsx'
xls = pd.ExcelFile(file_path)

# 查看工作表名称
sheet_names = xls.sheet_names

# 从第一个工作表加载数据
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 过滤出日期在2023年6月24日至2023年6月30日之间的记录
df['日期'] = pd.to_datetime(df['日期'])
filtered_df = df[(df['日期'] >= '2023-06-24') & (df['日期'] <= '2023-06-30')]

# 过滤掉批发价格为空的行
filtered_df_with_prices = filtered_df.dropna(subset=['批发价格(元/千克)'])
filtered_df_with_prices['单品编码'] = filtered_df_with_prices['单品编码'].astype(str)

# 将结果保存为新的Excel文件
output_file_path = './问题三/筛选单品_进价.xlsx'
filtered_df_with_prices.to_excel(output_file_path, index=False)