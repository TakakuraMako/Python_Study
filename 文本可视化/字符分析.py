import re
import jieba
import matplotlib.pyplot as plt

# 配置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def clean_text(text):
    """
    清洗文本：保留标点符号，去掉特殊字符。
    """
    text = re.sub(r'[^\w\s。！？,，]', '', text)  # 只保留标点符号和字母、数字
    return text

def tokenize_text(text):
    """
    分词并去除停用词
    """
    stop_words = load_stopwords('./文本可视化/stopwords_hit.txt')  # 停用词文件路径
    tokens = jieba.cut(text)
    return [token for token in tokens if token not in stop_words and len(token) > 1]

def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())

def analyze_characters(text):
    """
    对文本进行字符分析。
    """
    total_chars = len(text)
    letters = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    spaces = sum(1 for char in text if char.isspace())
    punctuations = sum(1 for char in text if char in "，。！？；：")
    return total_chars, letters, digits, spaces, punctuations

def calculate_conformity(text):
    """
    计算文本的从众性，通过成词率和平均词长。
    """
    tokens = tokenize_text(text)
    total_chars = len(text)
    total_words = len(tokens)
    total_word_length = sum(len(word) for word in tokens)
    word_rate = total_word_length / total_chars if total_chars > 0 else 0
    avg_word_length = total_word_length / total_words if total_words > 0 else 0
    conformity = word_rate * avg_word_length
    return conformity, word_rate, avg_word_length

def calculate_fragmentation(text):
    """
    计算文本的句子破碎度。
    破碎度 = 句子中的停顿次数 / 总句数
    """
    sentences = re.split(r'[。！？]', text)  # 按标点符号分割句子
    stop_punctuations = '，、；：'
    total_stops = sum(sentence.count(p) for sentence in sentences for p in stop_punctuations)
    total_sentences = len(sentences)
    fragmentation = total_stops / total_sentences if total_sentences > 0 else 0
    return fragmentation

def character_analysis(file1_path, file2_path):
    """
    对两篇文章进行字符分析、从众性分析和句子破碎度分析。
    """
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        text1 = clean_text(f1.read())
        text2 = clean_text(f2.read())

    # 字符分析
    total1, letters1, digits1, spaces1, punctuations1 = analyze_characters(text1)
    total2, letters2, digits2, spaces2, punctuations2 = analyze_characters(text2)

    # 从众性分析
    conformity1, word_rate1, avg_word_length1 = calculate_conformity(text1)
    conformity2, word_rate2, avg_word_length2 = calculate_conformity(text2)

    # 句子破碎度分析
    fragmentation1 = calculate_fragmentation(text1)
    fragmentation2 = calculate_fragmentation(text2)

    # --- 绘制字符分布图 ---
    categories = ['字母', '数字', '空格', '标点符号']
    values1 = [letters1, digits1, spaces1, punctuations1]
    values2 = [letters2, digits2, spaces2, punctuations2]
    x = range(len(categories))
    plt.figure(figsize=(10, 6))
    plt.bar(x, values1, width=0.4, label='活着', color='blue', align='center')
    plt.bar([i + 0.4 for i in x], values2, width=0.4, label='透明的红萝卜', color='orange', align='center')
    plt.xticks([i + 0.2 for i in x], categories)
    plt.title('字符分布对比')
    plt.ylabel('数量')
    plt.legend()
    plt.show()

    # --- 绘制从众性分析图和句子破碎度分析图合并 ---
    conformity_labels = ['成词率', '平均词长', '从众性', '破碎度']
    conformity_values1 = [word_rate1, avg_word_length1, conformity1, fragmentation1]
    conformity_values2 = [word_rate2, avg_word_length2, conformity2, fragmentation2]
    
    x_conformity = range(len(conformity_labels))
    plt.figure(figsize=(10, 6))
    plt.bar(x_conformity, conformity_values1, width=0.4, label='活着', color='blue', align='center')
    plt.bar([i + 0.4 for i in x_conformity], conformity_values2, width=0.4, label='透明的红萝卜', color='orange', align='center')
    plt.xticks([i + 0.2 for i in x_conformity], conformity_labels)
    plt.title('从众性分析与句子破碎度对比')
    plt.ylabel('值')
    plt.legend()
    plt.show()


    return {
        "字符分析": {
            "活着": {
                "总字符数": total1,
                "字母数": letters1,
                "数字数": digits1,
                "空格数": spaces1,
                "标点符号数": punctuations1
            },
            "透明的红萝卜": {
                "总字符数": total2,
                "字母数": letters2,
                "数字数": digits2,
                "空格数": spaces2,
                "标点符号数": punctuations2
            }
        },
        "从众性分析": {
            "活着": {
                "成词率": word_rate1,
                "平均词长": avg_word_length1,
                "从众性": conformity1
            },
            "透明的红萝卜": {
                "成词率": word_rate2,
                "平均词长": avg_word_length2,
                "从众性": conformity2
            }
        },
        "句子破碎度": {
            "活着": fragmentation1,
            "透明的红萝卜": fragmentation2
        }
    }

# 示例使用
file1_path = './文本可视化/活着.txt'
file2_path = './文本可视化/透明的红萝卜.txt'
results = character_analysis(file1_path, file2_path)
print("分析结果：", results)
