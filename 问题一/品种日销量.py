import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False

file_path_processed = './问题一/单品日销量处理.xlsx'

# Read the data from the sheet
df_processed = pd.read_excel(file_path_processed)

df_processed['销售日期'] = pd.to_datetime(df_processed['销售日期'])
df_sorted = df_processed.sort_values(by=['品类名称', '销售日期'])

plt.figure(figsize=(12, 8))
for product in df_sorted['品类名称'].unique():
    product_data = df_sorted[df_sorted['品类名称'] == product]
    plt.plot(product_data['销售日期'], product_data['销量(千克)'], label=product)

plt.title('品类日销量折线图')
plt.xlabel('销售日期')
plt.ylabel('销量(千克)')
plt.legend(title='品类名称', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
