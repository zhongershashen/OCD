import random
import re

import requests
from lxml import etree

pattern = re.compile(r'<[^>]+>', re.S)

api_url = 'http://url2api.applinzi.com/article'  # URL2Article API地址，使用体验版或购买独享资源
# 体验版: http://url2api.applinzi.com/article
token = 'Sc4mvSPvTvSz3VabOOVV_g'  # 开发者 token, 注册后可得，注意保密
fields = ','.join(['next', ])  # 可选字段

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.50',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
all_ip_list = []
usable_ip_list = []


def get_ip_pool():
    for i in range(1, 8):
        response = requests.get(url=f'http://www.ip3366.net/free/?page={i}', headers=headers)
        text = response.text.encode('ISO-8859-1')
        html = etree.HTML(text)
        tr_list = html.xpath('/html/body/div[2]/div/div[2]/table/tbody/tr')
        for td in tr_list:
            ip_ = td.xpath('./td[1]/text()')[0]  # ip
            port_ = td.xpath('./td[2]/text()')[0]  # 端口
            proxy = ip_ + ':' + port_  # 115.218.5.5:9000
            all_ip_list.append(proxy)
            judge_ip(proxy)  # 开始检测获取到的ip是否可以使用
    print('抓取完成！')
    print(f'抓取到的ip个数为：{len(all_ip_list)}')
    print(f'可以使用的ip个数为：{len(usable_ip_list)}')
    print('分别有：\n', usable_ip_list)


def get_ip_local():
    with open('ipPool.txt', 'r') as f:
        for line in f.readlines():
            judge_ip(line.replace("\n",""))
        f.close()

def judge_ip(proxy):
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy,
    }
    print(proxies)
    try:
        response = requests.get(url='https://www.baidu.com/', headers=headers, proxies=proxies,
                                timeout=1)  # 设置timeout，使响应等待1s
        response.close()
        if response.status_code == 200:
            print(proxy, '\033[31m可用\033[0m')
        else:
            print(proxy, '不可用')
    except:
        print(proxy, '请求异常')


def search(key_word):
    base_url = 'https://www.baidu.com/s?ie=UTF-8&wd={}'.format(key_word)
    # proxy = random.choice(usable_ip_list)
    # proxies = {
    #     "http": "http://" + proxy,
    #     "https": "http://" + proxy,
    # }
    try:
        r = requests.get(base_url, headers=headers)
        r.encoding = 'utf-8'
        res = etree.HTML(r.text)
        selector = res.xpath('//div[@id="content_left"]/div[@class="result c-container xpath-log new-pmd"]')
        data_list = []
        for data in selector:
            item = {'title': ''.join(data.xpath('.//h3/a/text()')), 'link': ''.join(data.xpath('.//h3/a/@href'))}
            data_list.append(item)
    finally:
        return data_list


def get_main_content(url):
    query_string = {'token': token, 'url': url, 'fields': fields}
    ret = requests.get(api_url, params=query_string)
    res = ret.json()['content']
    return res


def get_url_content(keyword):
    res = []
    url_list = search(keyword)
    for url in url_list:
        content = pattern.sub('', get_main_content(url['link'])).replace('\n', '')
        temp = {'url': url['link'], 'content': content}
        res.append(temp)
    return res

