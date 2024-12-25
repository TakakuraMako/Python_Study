import pandas as pd
import plotly.express as px

# 读取 Excel 文件，假设文件名为 'universities.xlsx'，并且有一个名为 'Sheet1' 的工作表
df = pd.read_excel('qs/2024年QS世界大学排名（QS World University Rankings 2024）.xlsx')

# 查看数据的前几行，检查数据格式
print(df.head())

# 按排名筛选出前100所大学
top_100_universities = df[df['Rank'] <= 100]

# 统计每个Region的大学数量
region_counts = top_100_universities['Region'].value_counts().reset_index()
region_counts.columns = ['Region', 'Count']

# 绘制地理空间可视化
fig = px.choropleth(region_counts, 
                    locations="Region", 
                    color="Count", 
                    hover_name="Region", 
                    color_continuous_scale="Viridis",
                    title="Number of Top 100 Universities by Region")

# 显示地图
fig.show()
