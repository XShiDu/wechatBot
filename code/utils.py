# 在此文件编写更新数据的函数
import requests
import json

import yaml

with open('../api_config.yaml', 'r', encoding='utf-8') as f:
    apis = yaml.load(f.read(), Loader=yaml.FullLoader)
f.close()

def get_stock_industry(code, iscode):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    if iscode == '0':
        code = stock_map[code]


    url = f"{apis['stock_params']['stock_industry']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        conception = json.loads(response.text)
        res = f'{code}所属概念或行业包括：\n'
        for index, industry in enumerate(conception):
            res += f"{index + 1}、{industry['name']}\n"
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'