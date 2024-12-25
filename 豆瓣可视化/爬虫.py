import requests
import re
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
urlbase = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='
page = list(range(0, 20))
labels = ['bookname', 'author', 'year', 'score', 'population', 'url']
data = pd.DataFrame(columns=labels)
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
import requests
from fake_useragent import UserAgent
import re
import pandas as pd
from bs4 import BeautifulSoup
import time
# 设置代理
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'https://127.0.0.1:7890'}

# 请求头
headers = {'User-Agent': UserAgent().random}

# 创建会话对象
session = requests.Session()

# 配置会话的代理
session.proxies.update(proxies)

pattern1 = re.compile(r'<li\s+class="subject-item">.*?nbg" href="(?P<url>.*?)".*?title="(?P<bookname>.*?)".*?<div class="pub">(?P<author>.*?)\/.*?(?P<year>\d.*?)[^\d].*?rating_nums">(?P<score>\d.*?\d).*?\((?P<population>\d.*?)人', re.S)

for i in range(len(page)):
    url = urlbase + str(page[i] * 20) + '&type=T'
    response = session.get(url=url,headers=headers)
    print(response)
    response.encoding = response.apparent_encoding
    content = response.text

    matches1 = pattern1.finditer(content)
    for match1 in matches1:
        temp = pd.DataFrame(columns=labels,data=[[match1.group('bookname').strip(), match1.group('author').strip(), match1.group('year').strip(), match1.group('score').strip(), match1.group('population').strip(), match1.group('url').strip()]])
        data = pd.concat([data, temp])
    response.close()
    time.sleep(2)
    if i == 16:
        break
data.to_csv('book.csv', index=False, encoding='utf-8-sig')