# 导入必要的库
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.manifold import TSNE
import networkx as nx
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
# 定义函数：清理和分词文本
def tokenize_text(text):
    """
    将文本按句子和单词进行分割
    - 输入: text (str) 文本字符串
    - 输出: sentences (list) 句子列表, words (list) 单词列表
    """
    # 按中文句子分隔符拆分
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if s.strip()]  # 移除空白句子
    # 提取所有中文字符作为单词
    words = re.findall(r'[一-鿿]', text)
    return sentences, words

# 定义函数：绘制句子长度分布图
def plot_sentence_length_distribution(sentences1, sentences2, titles):
    """
    绘制两组句子长度分布的对比直方图
    - 输入: sentences1 (list) 第一组句子列表, sentences2 (list) 第二组句子列表, titles (list) 两组数据的标题
    """
    lengths1 = [len(s) for s in sentences1]
    lengths2 = [len(s) for s in sentences2]

    plt.hist(lengths1, bins=20, alpha=0.7, label=titles[0], color='blue')
    plt.hist(lengths2, bins=20, alpha=0.7, label=titles[1], color='green')

    plt.xlabel("句子长度")
    plt.ylabel("频率")
    plt.title("句子长度分布对比")
    plt.legend()
    plt.show()

# 定义函数：绘制句子长度分布的累积密度函数（CDF）
def plot_sentence_length_cdf(sentences1, sentences2, titles):
    lengths1 = [len(s) for s in sentences1]
    lengths2 = [len(s) for s in sentences2]

    sns.ecdfplot(lengths1, label=titles[0])
    sns.ecdfplot(lengths2, label=titles[1])

    plt.xlabel("句子长度")
    plt.ylabel("累积概率")
    plt.title("句子长度分布的累积密度函数（CDF）")
    plt.legend()
    plt.show()

# 定义函数：绘制高频词双轴对比条形图
def plot_dual_axis_bar_chart(words1, words2, title1, title2, top_n=10):
    freq1 = Counter(words1).most_common(top_n)
    freq2 = Counter(words2).most_common(top_n)

    labels1, values1 = zip(*freq1)
    labels2, values2 = zip(*freq2)

    x = range(len(labels1))

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.bar(x, values1, alpha=0.7, label=title1, color="blue", width=0.4)
    ax2.bar([i + 0.4 for i in x], values2, alpha=0.7, label=title2, color="green", width=0.4)

    ax1.set_ylabel(title1)
    ax2.set_ylabel(title2)
    plt.xticks([i + 0.2 for i in x], labels1, rotation=45)
    plt.title("高频词双轴对比")
    fig.legend()
    plt.show()

# 定义函数：词向量嵌入可视化（降维后）
def plot_word_embedding(words, title):
    word_freq = Counter(words)
    words_sample = list(word_freq.keys())[:100]  # 限制为前100个词

    vectors = np.random.rand(len(words_sample), 100)  # 随机生成词向量
    tsne = TSNE(n_components=2, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)

    plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], alpha=0.7)
    for i, word in enumerate(words_sample):
        plt.text(reduced_vectors[i, 0], reduced_vectors[i, 1], word, fontsize=8)
    plt.title(f"{title} 词向量嵌入可视化 (t-SNE 降维)")
    plt.show()

# 定义函数：共现网络图
def plot_co_occurrence_network(words, title, min_count=2, max_nodes=50):
    # 统计相邻词的共现次数
    co_occurrence = Counter(zip(words[:-1], words[1:]))
    
    # 过滤出共现次数大于min_count的词对
    edges = [(word1, word2, count) for (word1, word2), count in co_occurrence.items() if count >= min_count]
    
    # 创建图对象
    G = nx.Graph()
    for word1, word2, weight in edges:
        G.add_edge(word1, word2, weight=weight)
    
    # 获取高频词
    top_nodes = [node for node, degree in G.degree()][:max_nodes]  # 限制节点数目
    
    # 只保留高频词的节点和边
    G = G.subgraph(top_nodes)
    
    # 使用kamada_kawai_layout优化图的布局
    pos = nx.kamada_kawai_layout(G)
    
    plt.figure(figsize=(12, 12))
    
    # 根据边的权重调整颜色和宽度
    edges = G.edges(data=True)
    edge_width = [d['weight'] * 0.1 for (u, v, d) in edges]  # 边宽度和权重成正比
    edge_color = [d['weight'] for (u, v, d) in edges]  # 边颜色和权重成正比
    
    # 绘制图
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightblue", alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=edge_width, edge_color=edge_color, edge_cmap=plt.cm.Blues, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", font_weight="bold")
    
    plt.title(f"{title} 共现网络图", fontsize=16)
    plt.axis("off")  # 不显示坐标轴
    plt.show()


# 定义函数：统计并展示词频
def top_word_frequency(words, title, top_n=10):
    """
    显示文本中最高频词汇
    - 输入: words (list) 单词列表, title (str) 标题, top_n (int) 最高频的单词数量
    - 输出: 返回最高频词的统计结果
    """
    word_freq = Counter(words)  # 统计词频
    top_words = word_freq.most_common(top_n)  # 获取前top_n个高频词
    # 绘制条形图
    labels, values = zip(*top_words)
    plt.bar(labels, values, alpha=0.7)
    plt.xlabel("单词")
    plt.ylabel("频率")
    plt.title(f"{title} 的最高频词汇统计")
    plt.show()
    return top_words

# 定义函数：生成词云
def generate_wordcloud(words, title):
    """
    生成词云图
    - 输入: words (list) 单词列表, title (str) 图标题
    """
    word_freq = Counter(words)  # 统计词频
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/simsun.ttc", 
                           width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show()

# 定义函数：计算成词率和聚类度
def calculate_text_conformity(sentences, words):
    """
    计算文本的成词率和聚类度
    - 输入: sentences (list) 句子列表, words (list) 单词列表
    - 输出: 成词率 (float), 聚类度 (float)
    """
    total_characters = sum(len(s) for s in sentences)  # 文本总字符数
    total_words = len(words)  # 文本总词数
    average_word_length = np.mean([len(word) for word in words])  # 平均词长

    term_rate = total_words / total_characters  # 成词率
    clustering_degree = term_rate * average_word_length  # 聚类度
    return term_rate, clustering_degree

# 定义函数：统计句子破碎度
def calculate_sentence_fragmentation(sentences):
    """
    计算句子破碎度
    - 输入: sentences (list) 句子列表
    - 输出: 平均破碎度 (float)
    """
    total_pauses = sum(sentence.count(p) for sentence in sentences for p in "，、；：")  # 统计句中停顿符号
    fragmentation = total_pauses / len(sentences)  # 每句平均停顿符号数
    return fragmentation

# 定义函数：绘制对比图
def plot_comparison(x_labels, y_values1, y_values2, y_label, title, legend_labels):
    """
    绘制两组数据的对比柱状图
    - 输入: x_labels (list) x轴标签, y_values1 (list) 数据1, y_values2 (list) 数据2
             y_label (str) y轴标签, title (str) 图标题, legend_labels (list) 图例标签
    """
    x = np.arange(len(x_labels))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width/2, y_values1, width, label=legend_labels[0])
    bars2 = ax.bar(x + width/2, y_values2, width, label=legend_labels[1])

    ax.set_xlabel("指标")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend()

    plt.show()
# 使用数据进行分析
with open("./文本可视化/活着.txt", "r", encoding="utf-8") as f:
    huozhe_content = f.read()
with open("./文本可视化/透明的红萝卜.txt", "r", encoding="utf-8") as f:
    hongluobo_content = f.read()

# 对文本分词
huozhe_sentences, huozhe_words = tokenize_text(huozhe_content)
hongluobo_sentences, hongluobo_words = tokenize_text(hongluobo_content)

# 生成句子长度分布图
# plot_sentence_length_distribution(huozhe_sentences, hongluobo_sentences, ["活着", "透明的红萝卜"])

# 生成句子长度累积密度函数（CDF）
# plot_sentence_length_cdf(huozhe_sentences, hongluobo_sentences, ["活着", "透明的红萝卜"])

# 生成高频词双轴对比图
# plot_dual_axis_bar_chart(huozhe_words, hongluobo_words, "活着高频词", "透明的红萝卜高频词")

# 生成词向量嵌入可视化
# plot_word_embedding(huozhe_words, "活着")
# plot_word_embedding(hongluobo_words, "透明的红萝卜")

# 生成共现网络图
plot_co_occurrence_network(huozhe_words, "活着")
plot_co_occurrence_network(hongluobo_words, "透明的红萝卜")

# 生成词频统计和词云
# huozhe_top_words = top_word_frequency(huozhe_words, "活着")
# hongluobo_top_words = top_word_frequency(hongluobo_words, "透明的红萝卜")
# generate_wordcloud(huozhe_words, "活着的词云")
# generate_wordcloud(hongluobo_words, "透明的红萝卜的词云")

# 计算成词率和聚类度
# huozhe_term_rate, huozhe_clustering_degree = calculate_text_conformity(huozhe_sentences, huozhe_words)
# hongluobo_term_rate, hongluobo_clustering_degree = calculate_text_conformity(hongluobo_sentences, hongluobo_words)

# 计算句子破碎度
# huozhe_fragmentation = calculate_sentence_fragmentation(huozhe_sentences)
# hongluobo_fragmentation = calculate_sentence_fragmentation(hongluobo_sentences)

# 绘制成词率和聚类度对比图
# plot_comparison(
#     ["成词率", "聚类度"],
#     [huozhe_term_rate, huozhe_clustering_degree],
#     [hongluobo_term_rate, hongluobo_clustering_degree],
#     "值",
#     "成词率与聚类度对比",
#     ["活着", "透明的红萝卜"]
# )

# 绘制句子破碎度对比图
# plot_comparison(
#     ["句子破碎度"],
#     [huozhe_fragmentation],
#     [hongluobo_fragmentation],
#     "破碎度",
#     "句子破碎度对比",
#     ["活着", "透明的红萝卜"]
# )
