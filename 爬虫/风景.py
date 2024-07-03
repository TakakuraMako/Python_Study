import requests
import re
url = 'https://pic.netbian.com/4kfengjing/index'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
obj = re.compile(r'<li><a.*?><img\ssrc="(?P<img>.*?)".*?"(?P<name>.*?)"')
for page in range(1, 6):#只爬前三页
    if page == 1:
        resp = requests.get(url = url + '.html', headers=headers)
    else:
        resp = requests.get(url = url + f'_{str(page)}.html', headers=headers)
    resp.encoding = resp.apparent_encoding
    result = obj.finditer(resp.text)
    n = 1
    for i in result:
        pic = requests.get(url='https://pic.netbian.com'+i.group('img').strip())
        _ = i.group('name').strip()
        print(_)
        with open(f'./爬虫/picture/{page}_{n}.jpg','wb') as f:
            f.write(pic.content)
        n += 1
