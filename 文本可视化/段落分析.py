import re
import matplotlib.pyplot as plt

# 配置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def clean_text(text):
    """
    清洗文本：保留换行符和标点符号，去掉特殊字符。
    """
    text = re.sub(r'[^\w\s。！？,，\n]', '', text)
    text = re.sub(r'\u3000\u3000', '', text)  # 去掉段首多余空格
    return text

def split_paragraphs(text):
    """
    按换行符分割段落。
    """
    paragraphs = text.split('\n')
    return [para.strip() for para in paragraphs if para.strip()]

def paragraph_analysis(file1_path, file2_path):
    """
    对两篇文章进行段落分析。
    """
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        text1 = clean_text(f1.read())
        text2 = clean_text(f2.read())

    paragraphs1 = split_paragraphs(text1)
    paragraphs2 = split_paragraphs(text2)

    lengths1 = [len(re.split(r'[。！？]', para)) for para in paragraphs1]
    lengths2 = [len(re.split(r'[。！？]', para)) for para in paragraphs2]

    avg_length1 = sum(lengths1) / len(lengths1) if lengths1 else 0
    avg_length2 = sum(lengths2) / len(lengths2) if lengths2 else 0

    # 绘制段落长度分布图
    plt.figure(figsize=(10, 6))
    plt.hist(lengths1, bins=20, alpha=0.7, label='活着', color='blue')
    plt.hist(lengths2, bins=20, alpha=0.7, label='透明的红萝卜', color='orange')
    plt.title('段落长度分布对比')
    plt.xlabel('段落包含句子数')
    plt.ylabel('频数')
    plt.legend()
    plt.show()

    return {
        "活着": {
            "段落总数": len(lengths1),
            "平均段落句数": avg_length1
        },
        "透明的红萝卜": {
            "段落总数": len(lengths2),
            "平均段落句数": avg_length2
        }
    }

# 示例使用
file1_path = './文本可视化/活着.txt'
file2_path = './文本可视化/透明的红萝卜.txt'
paragraph_results = paragraph_analysis(file1_path, file2_path)
print("段落分析结果：", paragraph_results)
