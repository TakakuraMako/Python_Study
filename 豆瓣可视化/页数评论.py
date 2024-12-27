import requests
from fake_useragent import UserAgent
import re
import pandas as pd
from bs4 import BeautifulSoup
import time
data = pd.read_excel('./豆瓣可视化/book.xlsx')
# 设置代理
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'https://127.0.0.1:7890'}

# 请求头
headers = {'User-Agent': UserAgent().random}

# 创建会话对象
session = requests.Session()

# 配置会话的代理
session.proxies.update(proxies)

pattern = re.compile(r'<meta name="description" content=".*?短评。(?P<comment>.*?)"', re.S)
for i in range(184, 225):
    url = data.iloc[i]['url'] + 'comments/'

    # 发起请求
    response = session.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        print(i)
        break
    content = response.text
    matches = pattern.finditer(content)
    for match in matches:
        data.loc[i, 'comment'] = match.group('comment').strip()
        break
    response.close()
    time.sleep(2)
data.to_excel('./豆瓣可视化/book.xlsx', index=False)