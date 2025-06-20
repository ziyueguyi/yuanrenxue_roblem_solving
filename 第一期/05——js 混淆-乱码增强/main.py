import execjs
from curl_cffi import requests

cookies = {
    'sessionid': 'jwxet0idmq3dlrncz0qaep5g15hupbvw',
    'no-alert3': 'true',
    'm': 'edb5bad3e5b9786415bfa84a44d5a142',
    'RM4hZBv0dDon443M': 'MX3EAbNoN8K5XgqYE+PMINC65dn5k5+dya0WLG9zj8DevYpsT5dG/GjQSV9XABtM0NkwywHukWiQWrJmuGuGv5ELAAwwSudx80XQcQ7hsGJvyga9qdWc0QUvSiw4bfgeTEByqXy/oKXVRHfnAkfHtrj7P6D2S/QQanXoKDOZSovsUC0+OOQjnUfvr6jttbm68hJgQGyJlRtt0w4vZ/32hCQsHMUW/W9dvQesmHeC9Pw=',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh,zh-CN;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/5',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1749526096,1749538037,1749540164,1749609599; no-alert3=true; sessionid=jwxet0idmq3dlrncz0qaep5g15hupbvw; tk=-9006859064502646364; m=e3e1831147a2b8bbb57d5587412368df; RM4hZBv0dDon443M=QjKvOqsGsVAjXi35H9UGRNdAITk8IyCQ4trxXyyxYc/jzqrOxKsXcwoIeb81JCjp1iIPWJMprhyuKB+kkZ5PUgIVkekKdW9SfOGwoWemlms/OIWuKFkofVGk4+tF0b/pXAHzNzAFOYD2wsamZSvSW3U7BNJX8+N0udjZx5NzXJgARAW6Tfm4iPN/I0YwNWDiy0ueWifb5+QzAlT0+WRkui7GS4CFl0ENZibAIGVr+KU=',
}
session = requests.Session()
session.cookies.update(cookies)
session.headers.update(headers)
with open('files/decode.js', 'r', encoding='utf-8') as f:
    encrypt = f.read()
    encrypt_fun = execjs.compile(encrypt)
num_list = []
total_num=0
for i in range(1, 6):
    result = encrypt_fun.call('get_aes')
    params = {
        'page': i,
        'm': result.get('m'),
        'f': result.get('f'),
    }
    session.cookies = {
        'sessionid': session.cookies.get('sessionid'),
        'm': result.get('cookie_m'),
        'no-alert3': 'true',
        'RM4hZBv0dDon443M': result.get('rm4'),
    }
    response = session.get('https://match.yuanrenxue.cn/api/match/5', params=params)
    if response.text:
        num_list.extend([item.get("value") for item in response.json().get("data")])
print(num_list)
total_num = sum(list(sorted(num_list,reverse=True))[0:5])
print(total_num)
