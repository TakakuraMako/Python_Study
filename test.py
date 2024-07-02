import requests

base_url = 'https://tianqi.2345.com/Pc/GetHistory'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Cookie': 'Hm_lvt_a3f2879f6b3620a363bec646b7a8bcdd=1719905124; lastCountyId=54511; lastCountyPinyin=beijing; lastProvinceId=12; lastCityId=54511; Hm_lpvt_a3f2879f6b3620a363bec646b7a8bcdd=1719917404; lastCountyTime=1719917404',
    'Pragma': 'no-cache',
    'Referer': 'https://tianqi.2345.com/wea_history/54511.htm?year=2023&month=2',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest'
}

params = {
    'areaInfo[areaId]': 54511,
    'areaInfo[areaType]': 2,
    'date[year]': 2023,
    'date[month]': 7,
}

# 发送请求
response = requests.get(base_url, headers=headers, params=params)
response.encoding = response.apparent_encoding

# 打印响应内容
print(response.text)
