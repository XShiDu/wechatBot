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

def get_history_supervisors(code, iscode):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]

    url = f"{apis['stock_params']['history_supervisors']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        history = json.loads(response.text)
        res = f'{code}的在职监事会成员包括：\n'
        now = datetime.now().strftime('%Y-%m-%d')
        for director in history:
            if director['edate'] > now:
                res += f"{director['title']}:{director['name']} {director['sdate']}~{director['edate']}\n"
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

def get_history_share(code, iscode, start_year=None, end_year=None):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]
    if not start_year:
        cur_year = datetime.now().year
        start_year = str(cur_year - 1)
        end_year = str(cur_year)

    url = f"{apis['stock_params']['history_share']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        history = json.loads(response.text)
        if start_year == end_year:
            res = f'{code}的{start_year}年分红如下：\n'
        else:
            res = f'{code}的{start_year}年~{end_year}年分红如下：\n'
        for share in history:
            if start_year <= share['sdate'][:4] <= end_year:
                res += f"公告日期：{share['sdate']}\n每10股送股:{share['give']}股\n每10股转增:{share['change']}股\n" \
                       f"每10股派息：{share['send']}元\n进度：{share['line']}\n除权除息日:{share['cdate']}\n" \
                       f"股权登记日：{share['edate']}\n红股上市日：{share['hdate']}\n\n"
        if "公告日期" not in res: res += '无'
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

def get_history_seo(code, iscode, start_year=None, end_year=None):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]
    if not start_year:
        cur_year = datetime.now().year
        start_year = str(cur_year - 1)
        end_year = str(cur_year)

    url = f"{apis['stock_params']['history_SEO']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        history = json.loads(response.text)
        if start_year == end_year:
            res = f'{code}的{start_year}年增发如下：\n'
        else:
            res = f'{code}的{start_year}年~{end_year}年增发如下：\n'
        for share in history:
            if start_year <= share['sdate'][:4] <= end_year:
                res += f"公告日期：{share['sdate']}\n发行方式:{share['type']}\n发行价格:{share['price']}元\n" \
                       f"实际公司募集资金总额：{share['tprice']}元\n发行费用总额：{share['fprice']}\n" \
                       f"实际发行数量:{share['amount']}\n\n"
        if "公告日期" not in res: res += '无'
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

def restrict_stock_open(code, iscode, start_year=None, end_year=None):

    with open('../data/stocksNameCode.yml', 'r', encoding='utf-8') as f:
        stock_map = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()
    with open('../api_config.yaml', 'r', encoding='utf-8') as f:
        apis = yaml.load(f.read(), Loader=yaml.FullLoader)
    f.close()

    if iscode == '0':
        code = stock_map[code]
    if not start_year:
        cur_year = datetime.now().year
        start_year = str(cur_year - 1)
        end_year = str(cur_year)

    url = f"{apis['stock_params']['restrict_stock_open']}/{code}/{apis['stock_params']['licence']}"
    response = requests.get(url)

    if response.status_code == 200:
        history = json.loads(response.text)
        if start_year == end_year:
            res = f'{code}的{start_year}年解禁限售如下：\n'
        else:
            res = f'{code}的{start_year}年~{end_year}年解禁限售如下：\n'
        for share in history:
            if start_year <= share['rdate'][:4] <= end_year:
                res += f"解禁日期：{share['rdate']}\n解禁数量(万股):{share['ramount']}\n解禁股流通市值(亿元):" \
                       f"{share['rprice']}\n上市批次：{share['batch']}\n公告日期：{share['pdate']}\n\n"
        if "公告日期" not in res: res += '无'
        return 'text', res,
    else:
        return 'text', '获取失败，请输入正确的代码或股票名称，或联系管理员查看接口是否正确'

print(restrict_stock_open('大理药业', '0', '2021', '2024')[1])