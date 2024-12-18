import pandas as pd  # 导入pandas库，用于处理数据
from pyecharts import options as opts  # 导入pyecharts的选项模块，用于设置图表选项
from pyecharts.charts import Map, Timeline  # 导入pyecharts的地图和时间轴图表模块
from itertools import chain  # 导入chain模块，用于展开嵌套列表

def timeline_map() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="1525px", height="725px"))  # 初始化时间轴组件，并设置宽度和高度

    tl.add_schema(
        play_interval=1000,  # 设置时间轴的播放间隔为1000毫秒
        pos_left="200",  # 设置时间轴在图表中的左边距
        pos_bottom="20",  # 设置时间轴在图表中的下边距
        label_opts=opts.LabelOpts(is_show=True, color="black"),  # 设置时间轴标签显示并指定颜色
    )

    # 读取CSV文件并加载为DataFrame，跳过前3行表头
    gdp = pd.DataFrame(pd.read_csv("./世界GDP/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_422027.csv", header=3))
    givegdp = ['Country Name']  # 初始化需要的列名列表，包含"国家名称"

    for x in range(1978, 2019):
        givegdp.append(str(x))  # 将1978到2018年的年份作为字符串添加到列名列表中

    # 提取指定列的数据，包括国家名称和每年的GDP
    locgdp = gdp.loc[:, givegdp]
    country = locgdp.loc[:, ['Country Name']]  # 提取国家名称列
    country = list(chain.from_iterable(country.values))  # 将嵌套列表展开为一维列表

    for y in range(1978, 2019):  # 按年度循环处理
        money = locgdp.loc[:, [str(y)]]  # 提取当年的GDP数据
        values = list(chain.from_iterable(money.values // 100000000))  # 将GDP值转换为单位"亿美元"

        # 创建世界地图图表
        map0 = (
            Map()
            .add(
                "GDP", [list(z) for z in zip(country, values)], "world", zoom=1.5  # 绑定国家名称和GDP值
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, font_size=10))  # 设置标签显示和字体大小
            .set_global_opts(
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="15%", pos_left="2%", is_show=False  # 设置图例位置和隐藏
                ),
                title_opts=opts.TitleOpts(
                    title="{}年世界各国经济总量（GDP）".format(y),  # 设置图表标题，显示当前年份
                    title_textstyle_opts=opts.TextStyleOpts(font_size=25, color="black")  # 设置标题字体大小和颜色
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_calculable=True,  # 设置颜色映射可计算
                    dimension=0,  # 指定维度
                    pos_left="100",  # 设置映射条左边距
                    pos_top="500",  # 设置映射条上边距
                    range_text=["单位亿美元", ""],  # 设置映射条的文本显示
                    range_color=["lightskyblue", "yellow", "orangered"],  # 设置颜色范围
                    textstyle_opts=opts.TextStyleOpts(color="black"),  # 设置映射条文本颜色
                    max_=150000, min_=1  # 设置映射条的最大值和最小值
                )
            )
        )
        tl.add(map0, "{}年".format(y))  # 将年度地图添加到时间轴中
    return tl  # 返回完整的时间轴图表

# 输出HTML文件
timeline_map().render("./世界GDP/world_gdp_map.html")  # 渲染图表为HTML文件，保存到指定路径
