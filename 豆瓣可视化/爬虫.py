import requests
import re
from fake_useragent import UserAgent
url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='
page = list(range(0, 20))

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
for i in range(len(page)):
    url += str(page[i] * 20) + '&type=T'
    response = requests.get(url=url,headers=headers)
    response.encoding = response.apparent_encoding
    content = response.text
    # 打印响应状态码和内容
    # print("Status Code:", response.status_code)
    # break
    obj = re.compile(r'<br>(?P<year>\d{4})&nbsp;/&nbsp;', re.S)
    result = obj.finditer(content)

    for i in result:
        #print(i.group('title').strip())
        print(i.group('year').strip())
    '''
    with open('douban.html', 'w', encoding='utf-8') as f:
        f.write(content)
        '''
    response.close()