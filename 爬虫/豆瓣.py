import requests
url = 'https://movie.douban.com/chart'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
param = {
    'type': 24,
    'interval_id': '100:90',
    'action': '',
    'start': 0,
    'limit': 20,
}
response = requests.get(url=url,params=param,headers=headers)
response.encoding = response.apparent_encoding
# 打印响应状态码和内容
print("Status Code:", response.status_code)
with open('douban.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
response.close()