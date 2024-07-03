import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'token': '3213401d93ad9be6cbd4d5fe788a1eaaf19e9b2f3dea45161c6b934e77e70b60',
    'cookie': 'zkhanecookieclassrecord=%2C66%2C53%2C; PHPSESSID=paahb3ftbusrnae6oc16u12a57; zkhanmlusername=%D3%A5%B2%D6%DC%D4%D7%D3; zkhanmluserid=7656247; zkhanmlgroupid=1; zkhanmlrnd=Jwv7bCp7mbYgXOjAS7d4; zkhanmlauth=15838654bb92530b8c22a4ef8e561bde'
}
url = 'https://pic.netbian.com/e/extend/downpic.php?'

resp = requests.get(url=url, headers=headers)
print(resp.text)
with open('test.jpg','wb') as f:
    f.write(resp.content)