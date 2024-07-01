import requests
kw = input()
url = f'https://fanyi.baidu.com/sug'
#dic = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"}
dic = {'kw' : kw}
response = requests.post(url, data=dic)
response.encoding = response.apparent_encoding
response_json = response.json()
#print(response)
out = []
#print(f'输入{kw}')
print('输出:')
for i in range(len(response_json['data'])):
    print(response_json['data'][i]['v'])
response.close()