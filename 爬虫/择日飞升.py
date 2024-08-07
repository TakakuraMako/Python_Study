import requests
import os
import re
import time
import random
from fake_useragent import UserAgent
url_list = 'http://www.xsbiquge.la/book/28880/'
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
headers={'User-Agent':UserAgent().random}
proxies = {
            'http': 'http://{}'.format('127.0.0.1:7890'),
            'https': 'https://{}'.format('127.0.0.1:7890'),
        }

dict = {}
link_re = re.compile(r'<dd>[\s\S]*?href="(?P<link>[\w/.]*)">[\n\r]* *(?P<title>第[\s\S]*?)[\n\r]')
content_re = re.compile(r'<p class="content_detail">[\r\n]* *(?P<content>[\s\S]*?[\r\n]+)')

resp_list = requests.get(url=url_list, headers=headers, proxies=proxies)
resp_list_text = resp_list.text
resp_list_text = re.sub(r'择日飞升最新6章[\s\S]*?择日飞升正文', '', resp_list_text)
result_re = link_re.finditer(resp_list_text)
for i in result_re:
    link = i.group('link').strip()
    title = i.group('title').strip()
    dict[title] = link
    
num = 1
content = ''
url_chapter = 'http://www.xsbiquge.la' + dict[list(dict.keys())[0]]
resp_content = requests.get(url = url_chapter, headers=headers, proxies=proxies)
resp_content.encoding = resp_content.apparent_encoding
for title in dict:
    url_chapter = 'http://www.xsbiquge.la' + dict[title]
    resp_content = requests.get(url = url_chapter, headers=headers, proxies=proxies)
    print(resp_content)
    result = content_re.finditer(resp_content.text)
    content += title + '\n'
    for i in result:
        content += i.group('content').strip() + '\n'
    content += '\n'
    sleeptime = random.randint(1, 10)
    print(num)
    time.sleep(sleeptime)
    num += 1

with open('飞升.txt', 'w', encoding=resp_content.encoding) as f:
    f.write(content)
