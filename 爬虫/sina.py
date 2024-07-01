import requests
import re
p = 1
url = 'https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

obj = re.compile(r'<tr><td .*?><a .*?>(?P<code>\d{6})</a></td><td .*?><a .*?>(?P<name>.*?)</a></td><td .*?>(?P<num>\d+)</td><td .*?>(?P<change>\d+)</td><td>(?P<Shareholding ratio>\d+)</td>
                 <td>-2.64</td>
                 <td>10.95</td>
                 <td>-2.73</td>           	<td><a href="javascript:void(0);"
                 onclick="showDetail('000526','20241',this);return false;">+展开明细</a></td>
                 </tr>')
resp = requests.get(url=url, headers=headers)
resp.encoding = resp.apparent_encoding
#print(resp)
with open('新浪股票.html', 'w', encoding=resp.encoding) as f:
    f.write(resp.text)