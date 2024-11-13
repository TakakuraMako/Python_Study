import requests
import re
import pandas as pd

url = 'https://tianqi.2345.com/Pc/GetHistory'

code = ['54511', '58362', '59287', '59493']
cities = ['北京', '上海', '广州', '深圳']
lable = ['日期', '星期', '最高温', '最低温', '天气', '风力风向', '空气质量指数']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Referer': 'https://tianqi.2345.com/wea_history/54511.htm?year=2023&month=2',
}

params = {
    'areaInfo[areaId]': 54511,
    'areaInfo[areaType]': 2,
    'date[year]': 2016,
    'date[month]': 7,
}

obj = re.compile(r'(?P<date>2016-\d\d-\d\d)\s(?P<week>.*?)<[\s\S]*?">(?P<higest>.*?)<[\s\S]*?;.*?>(?P<lowest>.*?)<[\s\S]*?<td>(?P<weather>.*?)<[\s\S]*?<td>(?P<wind>.*?)<[\s\S]*?">(?P<air>.*?)<')

for city in range(len(cities)):
    params['areaInfo[areaId]'] = code[city]
    data = pd.DataFrame(columns=lable)
    count = 0
    for month in range(1,13):
        params['date[month]'] = month
        response = requests.get(url, headers=headers, params=params)
        response.encoding = response.apparent_encoding
        html_content = response.json()['data']
        result = obj.finditer(html_content)
        for i in result:
            new = pd.DataFrame([[i.group('date').strip(), i.group('week').strip(), i.group('higest').strip(), i.group('lowest').strip(), i.group('weather').strip(), i.group('wind').strip(), i.group('air').strip()]],columns=lable)
            data = pd.concat([data,new])
    data['日期'] = '\t' + data['日期']
    data.to_csv(f'2016weather{cities[city]}.csv',encoding='GBK',index=None)
    break



