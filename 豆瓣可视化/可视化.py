import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import jieba
import re
import numpy as np
from matplotlib import cm
import matplotlib.patheffects as path_effects
import plotly.express as px
from imageio import imread
# 使plt支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_excel('./豆瓣可视化/book.xlsx')
data['author'] = data['author'].str.replace(r'\[.*?\]\s*', '', regex=True)
# 数据初探
# print(data.head())
# # 绘制竖向评分小提琴图
# plt.figure(figsize=(4, 6))
# sns.violinplot(
#     y='population',
#     x=None,  # 明确不使用 x 轴分类
#     data=data,
#     palette='Pastel1',  # 使用柔和配色
#     inner='quartile',   # 显示四分位数
#     linewidth=1.2,       # 调整边缘线的宽度
# )
# sns.despine(left=True)  # 去除左侧和顶部的边框
# plt.title('评分分布', fontsize=16, fontweight='bold')  # 美化标题
# plt.ylabel('评分人数', fontsize=12)  # 添加纵轴标签
# plt.xlabel('分布密度', fontsize=12)  # 添加横轴标签
# plt.grid(axis='x', linestyle='--', alpha=0.7)  # 添加网格线
# plt.xticks(fontsize=10)  # 调整横轴字体大小
# plt.yticks(fontsize=10)  # 调整纵轴字体大小
# plt.show()

# # 绘制评分词云图
# comment = ' '.join(data['comment'])
# comment = re.sub(r'[^\w\s。！？,，]', '', comment)  # 只保留标点符号和字母、数字
# def load_stopwords(filepath):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         return set(f.read().splitlines())
    
# def tokenize_text(text):
#     """
#     分词并去除停用词
#     """
#     stop_words = load_stopwords('./豆瓣可视化/stopwords_hit.txt')  # 停用词文件路径
#     tokens = jieba.cut(text)
#     filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
#     return filtered_tokens

# comment = tokenize_text(comment)
# comment = ' '.join(comment)
# # mask_image = imread("./豆瓣可视化/书.jpg")
# wordcloud = WordCloud(font_path='./豆瓣可视化/华文行楷.ttf', background_color='white').generate(comment)
# plt.imshow(wordcloud)
# plt.axis('off')
# plt.show()

# # 年度趋势：分析每年的平均评分和书籍数量
# yearly_trends = data.groupby('year').agg({
#     'score': 'mean',
#     'bookname': 'count'
# }).rename(columns={'score': '平均评分', 'bookname': '书籍数量'}).reset_index()
# # 按书籍数量占比排序并合并小于1%的年份
# yearly_trends['占比'] = yearly_trends['书籍数量'] / yearly_trends['书籍数量'].sum()
# sorted_trends = yearly_trends.sort_values(by='占比', ascending=False).reset_index(drop=True)

# # 合并小于1%的年份
# threshold = 0.01
# others = sorted_trends[sorted_trends['占比'] < threshold].copy()
# others_combined = pd.DataFrame({
#     'year': ['其他'],
#     '书籍数量': [others['书籍数量'].sum()],
#     '占比': [others['占比'].sum()]
# })

# # 合并数据
# main_trends = sorted_trends[sorted_trends['占比'] >= threshold]
# final_trends = pd.concat([main_trends, others_combined], ignore_index=True)

# colors = cm.viridis_r([i / len(final_trends) for i in range(len(final_trends))])

# # 绘制美化的饼图
# plt.figure(figsize=(10, 10))
# explode = [0.1 if i == final_trends['书籍数量'].max() else 0 for i in final_trends['书籍数量']]
# wedges, texts, autotexts = plt.pie(
#     final_trends['书籍数量'],
#     labels=None,  # 不直接显示标签
#     autopct=lambda p: f'{p:.1f}%' if p > 1 else '',  # 仅显示大于1%的标签
#     startangle=90,  # 调整起始角度
#     colors=colors,
#     explode=explode,
#     textprops={'fontsize': 15},
#     pctdistance=0.85
# )

# # 添加引导线和年份标签
# for i, (wedge, label) in enumerate(zip(wedges, final_trends['year'])):
#     angle = (wedge.theta2 + wedge.theta1) / 2  # 扇形中点角度
#     x = 1.2 * np.cos(np.radians(angle))  # 调整 x 坐标
#     y = 1.2 * np.sin(np.radians(angle))  # 调整 y 坐标
#     horizontal_alignment = 'left' if angle < 180 else 'right'
#     plt.annotate(
#         label, 
#         xy=(np.cos(np.radians(angle)), np.sin(np.radians(angle))),
#         xytext=(x, y),
#         textcoords='data',
#         ha=horizontal_alignment,
#         fontsize=15,
#         color='darkblue',
#         arrowprops=dict(arrowstyle="-", color='gray', lw=1)
#     )

# # 调整标签文字样式
# for text in texts:
#     text.set_color("darkblue")
#     text.set_fontsize(15)

# # 添加百分比文字黑色轮廓
# for autotext in autotexts:
#     autotext.set_color("white")
#     autotext.set_fontsize(15)
#     autotext.set_fontweight("bold")
#     autotext.set_path_effects([
#         path_effects.Stroke(linewidth=1, foreground="black"),  # 黑色轮廓
#         path_effects.Normal()
#     ])

# # 添加中央圆环，创建甜甜圈图效果
# centre_circle = plt.Circle((0, 0), 0.70, fc='white')
# plt.gca().add_artist(centre_circle)

# # 添加标题
# plt.title('年度书籍数量占比', fontsize=18, fontweight='bold', color='darkblue')
# plt.tight_layout()
# plt.show()


# # 图2: 年度平均评分
# plt.figure(figsize=(12, 6))
# plt.plot(yearly_trends['year'], yearly_trends['平均评分'], marker='o', color='orange', label='平均评分', linewidth=2)
# plt.title('年度平均评分趋势', fontsize=16, fontweight='bold')
# plt.xlabel('年份', fontsize=12)
# plt.ylabel('平均评分', fontsize=12)
# plt.legend()
# plt.grid(alpha=0.5, linestyle='--')
# plt.xlim([data['year'].min(), data['year'].max()])
# plt.xticks(range(data['year'].min(), data['year'].max() + 1, 1), rotation=45, fontsize=13)
# plt.tight_layout()
# plt.show()


# # 作者分析：统计每位作者的书籍数量及平均评分
# author_analysis = data.groupby('author').agg({
#     'bookname': 'count',
#     'score': 'mean'
# }).rename(columns={'bookname': '书籍数量', 'score': '平均评分'}).sort_values(by='书籍数量', ascending=False)

# # 展示前10位作者的书籍数量和评分
# top_authors = author_analysis.head(10).reset_index()
# # 作者分析图
# plt.figure(figsize=(12, 10))  # 增加图表宽度
# sns.barplot(x='author', y='书籍数量', data=top_authors, palette='viridis', alpha=0.8)
# plt.plot(top_authors['author'], top_authors['平均评分'], marker='o', color='red', label='平均评分')
# plt.title('作者书籍数量及平均评分（Top 10）', fontsize=16, fontweight='bold')
# plt.xlabel('作者', fontsize=13)
# plt.ylabel('数量 / 平均评分', fontsize=13)
# plt.legend()
# plt.grid(alpha=0.5, linestyle='--')
# plt.xticks(rotation=45, fontsize=15)  # 轻微旋转以节省空间
# plt.tight_layout()
# plt.show()

# 按年份汇总评分人数
yearly_population = data.groupby('year')['population'].sum().reset_index()

# 按年份汇总评分人数
yearly_population = data.groupby('year')['population'].sum().reset_index()

# 美化评分人数玫瑰图
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

# 转换角度为弧度
angles = np.linspace(0, 2 * np.pi, len(yearly_population), endpoint=False)
values = yearly_population['population']

# 绘制玫瑰图
bars = ax.bar(
    angles, values, width=2 * np.pi / len(yearly_population), bottom=0,
    color=plt.cm.viridis(values / max(values)), edgecolor='black', alpha=0.9
)

# 设置图表属性
ax.set_theta_offset(np.pi / 2)  # 起始角度调整
ax.set_theta_direction(-1)  # 顺时针方向

# 添加年份标签
ax.set_xticks(angles)
ax.set_xticklabels(
    yearly_population['year'], fontsize=12, color='darkblue', rotation=45, fontweight='bold'
)

# 去除径向刻度并美化
ax.set_yticks([])
ax.spines['polar'].set_visible(False)

# 创建颜色图例并附加到当前图形
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(values), vmax=max(values)))
sm.set_array([])
fig.colorbar(sm, ax=ax, pad=0.1, shrink=0.8, aspect=20, orientation='vertical').set_label(
    '评分人数', fontsize=14, color='darkblue', fontweight='bold'
)

# 添加标题
plt.title('年度评分人数变化（玫瑰图）', fontsize=18, fontweight='bold', color='darkblue', pad=20)
plt.tight_layout()
plt.show()


