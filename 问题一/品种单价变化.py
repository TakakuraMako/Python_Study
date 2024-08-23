import pandas as pd
data = pd.read_excel('附件3.xlsx')

# Extract the relevant columns
new = data.groupby(['日期', '分类名称'])['批发价格(元/千克)'].mean().reset_index()
# Save the filtered data to a new Excel file
output_file_path = '批发随日期变化.xlsx'
new.to_excel(output_file_path, index=False)

