import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
# 使plt支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_excel('./豆瓣可视化/book.xlsx')

# 数据初探
# print(data.head())

# 评分人数分布，使用小提琴图
plt.figure()
sns.violinplot(x=data['population'])
plt.xlabel('评分人数')
plt.title('评分人数分布')
plt.show()