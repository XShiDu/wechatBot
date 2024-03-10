# 在此文件编写更新数据的函数
import requests
import json
from datetime import datetime

import yaml

def get_stock_industry(code, iscode):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
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


def get_company_info(code, iscode):
    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]

    info_map = {'name':'公司名称', 'ename':'公司英文名称', 'market':'上市市场', 'idea':'概念及板块', 'ldate':'上市日期',
                'sprice':'发行价格（元）', 'principal':'主承销商', 'rdate':'成立日期', 'rprice':'注册资本',
                'instype':'机构类型', 'organ':'组织形式', 'secre':'董事会秘书', 'phone':'公司电话', 'sphone':'董秘电话',
                'fax':'公司传真', 'sfax':'董秘传真', 'email':'公司电子邮箱', 'semail':'董秘电子邮箱', 'site':'公司网站',
                'post':'邮政编码', 'infosite':'信息披露网址', 'oname':'证券简称更名历史', 'addr':'注册地址', 'oaddr':'办公地址',
                'desc':'公司简介', 'bscope':'经营范围', 'printype':'承销方式', 'referrer':'上市推荐人', 'putype':'发行方式',
                'pe':'发行市盈率（按发行后总股本）', 'firgu':'首发前总股本（万股）', 'lastgu':'首发后总股本（万股）',
                'realgu':'实际发行量（万股）', 'planm':'预计募集资金（万元）', 'realm':'实际募集资金合计（万元）',
                'pubfee':'发行费用总额（万元）', 'collect':'募集资金净额（万元）', 'signfee':'承销费用（万元）',
                'pdate':'招股公告日'}

    url = f"{apis['stock_params']['firm_detail']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        company_info = json.loads(response.text)
        info = [f"{info_map[key]}:{value}" for key, value in company_info.items()]

        res = f"{code}基本信息如下：\n"
        for info_ in info:
            res += f"{info_}\n"
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

def get_stock_index(code, iscode):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]

    url = f"{apis['stock_params']['belong_index']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        index = json.loads(response.text)
        res = f'{code}所属指数包括：\n'
        for i, index_ in enumerate(index):
            res += f"{i + 1}、{index_['mc']}({index_['dm']})\n"
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'


def get_history_manager(code, iscode):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]

    url = f"{apis['stock_params']['history_manager']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        history = json.loads(response.text)
        res = f'{code}的在职高管成员包括：\n'
        for manager in history:
            if manager['edate'] == '--':
                res += f"{manager['title']}:{manager['name']} {manager['sdate']}~至今\n"
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

def get_history_director(code, iscode):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]

    url = f"{apis['stock_params']['history_director']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        history = json.loads(response.text)
        res = f'{code}的在职董事会成员包括：\n'
        now = datetime.now().strftime('%Y-%m-%d')
        for director in history:
            if director['edate'] > now:
                res += f"{director['title']}:{director['name']} {director['sdate']}~{director['edate']}\n"
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

# print(get_history_director('大理药业', '0'))