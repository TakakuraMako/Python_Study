import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'referer': 'https://book.jd.com/'
}
url = 'https://gw-e.jd.com/client.action'
books_info = []

for i in range(1, 6):
    body = json.dumps({"moduleType": 1, "page": i, "pageSize": 20, "scopeType": 1})  # JSON格式的字符串作为请求参数
    params = {
        "callback": "func",
        "body": body,
        "functionId": "bookRank",
        "client": "e.jd.com",
    }
    resp = requests.get(url=url, params=params, headers=headers)
    
    # 移除JSONP回调函数
    jsonp_text = resp.text
    json_text = re.search(r'func\((.*)\)', jsonp_text).group(1)
    
    # 解析JSON数据
    data = json.loads(json_text)
    
    # 获取 'data' 部分
    books = data['data']['books']
    for book in books:
        book_id = book['bookId']
        book_name = book['bookName']
        publisher = book['publisher']
        item_url = f'https://item.jd.com/{book_id}.html'
        sell_price = book['sellPrice']
        define_price = book['definePrice']
        
        # 确保所有字段为字符串
        book_id = str(book_id)
        book_name = str(book_name)
        publisher = str(publisher)
        item_url = str(item_url)
        sell_price = str(sell_price)
        define_price = str(define_price)
        
        books_info.append((book_id, book_name, sell_price, define_price, publisher, item_url))

# 打印获取的书籍信息
for book in books_info:
    print(book)
