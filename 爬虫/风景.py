import requests
import re
url = 'https://pic.netbian.com/4kfengjing/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

resp = requests.get(url = url, headers=headers)
resp.encoding = resp.apparent_encoding
obj = re.compile(r'<li><a.*?><img\ssrc="(?P<img>.*?)".*?"(?P<name>.*?)"')
result = obj.finditer(resp.text)
n = 1
for i in result:
    pic = requests.get(url='https://pic.netbian.com'+i.group('img').strip())
    _ = i.group('name').strip()
    print(_)
    with open(f'./爬虫/picture/{n}.jpg','wb') as f:
        f.write(pic.content)
    n += 1
