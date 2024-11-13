import requests
import re
import pandas as pd

url = 'https://tianqi.2345.com/Pc/GetHistory'
year = list(range(2011, 2024, 1))
code = ['54511']
cities = ['北京']
lable = ['日期', '最高温', '最低温']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Referer': 'https://tianqi.2345.com/wea_history/54511.htm?year=2023&month=2',
}

for y in year:
    obj = re.compile(rf'(?P<date>{y}-\d\d-\d\d)\s(?P<week>.*?)<[\s\S]*?">(?P<higest>.*?)<[\s\S]*?;.*?>(?P<lowest>.*?)<[\s\S]*?<td>(?P<weather>.*?)<[\s\S]*?<td>(?P<wind>.*?)<[\s\S]*?">(?P<air>.*?)<'.format(y))
    params = {
        'areaInfo[areaId]': 54511,
        'areaInfo[areaType]': 2,
        'date[year]': y,
        'date[month]': 7,
    }
    data = pd.DataFrame(columns=lable)
    count = 0
    for month in range(1,13):
        params['date[month]'] = month
        response = requests.get(url, headers=headers, params=params)
        response.encoding = response.apparent_encoding
        html_content = response.json()['data']
        result = obj.finditer(html_content)
        for i in result:
            new = pd.DataFrame([[i.group('date').strip(), i.group('higest').strip(), i.group('lowest').strip()]],columns=lable)
            data = pd.concat([data,new])
    data['日期'] = '\t' + data['日期']
    # data['最高温'] = data['最高温'].str.replace('°', '').astype(int)
    # data['最低温'] = data['最低温'].str.replace('°', '').astype(int)
    # data['平均温度'] = (data['最高温'] + data['最低温']) / 2
    data.to_csv(f'{y}weather北京.csv',encoding='GBK',index=None)
    break


