import requests
import re
url = 'https://www.tianyancha.com/company/197257106'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
           'cookie': 'jsid=SEO-BING-ALL-SY-000001; TYCID=18a542903eae11ef91845df10999f6d2; CUID=5cd45a12147b26a3beb7e9b5555765df; ssuid=7269704442; sajssdk_2015_cross_new_user=1; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1720610313; HMACCOUNT=0D643829434DE5F4; _ga=GA1.2.721581353.1720610314; _gid=GA1.2.1641658771.1720610314; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22333551794%22%2C%22first_id%22%3A%221909c5dcd31136-03412d28f229ffe-4c657b58-960000-1909c5dcd33118%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkwOWM1ZGNkMzExMzYtMDM0MTJkMjhmMjI5ZmZlLTRjNjU3YjU4LTk2MDAwMC0xOTA5YzVkY2QzMzExOCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjMzMzU1MTc5NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22333551794%22%7D%2C%22%24device_id%22%3A%221909c5dcd31136-03412d28f229ffe-4c657b58-960000-1909c5dcd33118%22%7D; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2213795717586%22%2C%22userId%22:%22333551794%22}; tyc-user-info-save-time=1720610640065; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzc5NTcxNzU4NiIsImlhdCI6MTcyMDYxMDYyNiwiZXhwIjoxNzIzMjAyNjI2fQ.xYaPJIgf76UQjnw3rjISSVXMDXlFjmnkDQvKymPixL0zxMcF7Z7QsUFWyN5Qe7wgXWhN92MKgmyxUQKf0BB_Mg; tyc-user-phone=%255B%252213795717586%2522%255D; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1720614608'}
resp = requests.get(url=url, headers=headers)
resp.encoding = resp.apparent_encoding
print(resp)
'''
obj = re.compile(r'<span class="index_name.*?>(?P<name>.*?)<')

result = obj.finditer(resp.text)
for i in result:
    print(i.group('name').strip())
    '''

with open('test.txt', 'w', encoding=resp.encoding) as f :
    f.write(resp.text)