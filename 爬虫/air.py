import requests
import pandas as pd
import re
url = 'https://www.air-level.com/air/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
lable = ['beijing', 'shanghai', 'guangzhou', 'shenzhen']
obj = re.compile(r'<span class="aqi-bg aqi-level-1">(?P<air>.*?)</span>')
data = pd.DataFrame(columns=['air'],index=lable)
for i in range(len(lable)):
    resp = requests.get(url=url + lable[i], headers=headers)
    resp.encoding = resp.apparent_encoding
    result = obj.finditer(resp.text)
    for j in result:
        data.iloc[i,:] = j.group('air').strip()
print(data)