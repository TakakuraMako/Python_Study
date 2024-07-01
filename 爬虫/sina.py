import requests
import re
import pandas as pd
lable = ['证券代码','证券简称','机构数','机构数变化','持股比例','持股比例增幅','占流通股比例','占流通股比例增幅']
data = pd.DataFrame(columns=lable)
url = 'https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

obj = re.compile(r'<tr>[\s\S]*?<td[\s\S]*?"_blank">(?P<code>\d{6})</a>[\s\S]*?"_blank">(?P<name>.*?)<[\s\S]*?">(?P<num>\d+)[\s\S]*?">(?P<change>.*?)<[\s\S]*?<td>(?P<Shareholding_ratio>.*?)<[\s\S]*?<td>(?P<Shareholding_ratio_change>.*?)<[\s\S]*?<td>(?P<Percentage_of_outstanding_shares>.*?)<[\s\S]*?<td>(?P<Percentage_of_outstanding_shares_change>.*?)<')

for i in range(1, 72):
    resp = requests.get(url=url+ '?p=' + str(i), headers=headers)
    resp.encoding = resp.apparent_encoding
    result = obj.finditer(resp.text)
    for j in result:
        list = [j.group('code').strip(),j.group('name').strip(),j.group('num').strip(),j.group('change').strip(),j.group('Shareholding_ratio').strip(),j.group('Shareholding_ratio_change').strip(),j.group('Percentage_of_outstanding_shares').strip(),j.group('Percentage_of_outstanding_shares_change').strip()]
        data = pd.concat([data,pd.DataFrame([list],columns=lable)])
data['证券代码']='\t'+data['证券代码'] 
data.to_csv('sina.csv',encoding='GB18030',index=None)
