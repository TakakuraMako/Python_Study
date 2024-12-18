import pandas as pd
import json
import folium

# 读取地理信息文件路径
geo_data_path = './省级行政区.json'

# 读取地理信息文件
with open(geo_data_path, 'r', encoding='utf-8') as f:
    china_geo = json.load(f)

# 读取GDP数据文件路径
sheet_data_path = './省级gdp.xlsx'

# 读取Excel数据
sheet_data = pd.read_excel(sheet_data_path)

# 过滤年份列字段
years = [col for col in sheet_data.columns if '年' in col]

# 将GDP数据转为数字类型并实现数值统一
sheet_data[years] = sheet_data[years].apply(pd.to_numeric, errors='coerce')

# 创建基础地图
m = folium.Map(location=[35.0, 105.0], zoom_start=5, tiles="cartodbpositron")

# 为每个年份添加一个独立的图层
def add_gdp_layer(map_obj, year):
    folium.GeoJson(
        china_geo,
        style_function=lambda feature: {
            'fillColor': f"#{int(255 - (sheet_data.loc[sheet_data['name'] == feature['properties']['name'], year].values[0] / sheet_data[year].max()) * 255):02x}0000"
            if feature['properties']['name'] in sheet_data['name'].values else '#d3d3d3',
            'color': 'black',
            'weight': 0.2,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['name'],
            aliases=['Province:'],
            sticky=False
        ),
        name=f"GDP {year}"
    ).add_to(map_obj)

# 为每个年份生成一个图层
for year in years:
    add_gdp_layer(m, year)

# 添加图层控制器
folium.LayerControl().add_to(m)

# 保存地图到文件
output_path = "./china_gdp_interactive_map_dropdown.html"
m.save(output_path)

# 输出文件路径
print(output_path)
