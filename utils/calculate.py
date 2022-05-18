from utils import textProcess
from utils.scrapy import get_url_content
import Levenshtein

key = '人工智能（Artificial Intelligence）英文缩写为AI'


# 把content也分割成句子，取最大值
def cal_single(key_content_item, key):
    max_repeat = 0.0
    context = ''
    for item in textProcess.split_article(key_content_item['content']):
        temp = Levenshtein.jaro(key.strip(), item.strip())
        if temp > max_repeat:
            max_repeat = temp
            context = item
    return max_repeat, item


# 计算单句最高重复率
def get_single_repeat(key):
    global repeat_count
    global len_count
    key_content_list = get_url_content(key)
    max_repeat = 0.0
    url = ''
    web_content = ''
    for item in key_content_list:
        temp, temp_content = cal_single(item, key)
        if temp > max_repeat:
            max_repeat = temp
            url = item['url']
            web_content = temp_content

    return {'origin_text': key, 'repeat_ratio': max_repeat, 'url': url, "web_content": web_content}



# get_single_repeat(key)
# str1 = "人工智能（Artificial Intelligence）英文缩写为AI"
# str2 = "人工智能（Artificial Intelligence）英文为AI"
# # 1. difflib
# seq = difflib.SequenceMatcher(None, str1, str2)
# ratio = seq.quick_ratio()
# print('difflib', ratio)
#
# # 2. hamming距离，str1和str2长度必须一致，描述两个等长字串之间对应位置上不同字符的个数
# # sim = Levenshtein.hamming(str1, str2)
# # print 'hamming similarity: ', sim
#
# # 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
# sim = Levenshtein.distance(str1, str2)
# print('Levenshtein similarity: ', sim)
#
# # 4.计算莱文斯坦比
# sim = Levenshtein.ratio(str1, str2)
# print('Levenshtein.ratio similarity: ', sim)
#
# # 5.计算jaro距离
# sim = Levenshtein.jaro(str1, str2)
# print('Levenshtein.jaro similarity: ', sim)
#
# # 6. Jaro–Winkler距离
# sim = Levenshtein.jaro_winkler(str1, str2)
# print('Levenshtein.jaro_winkler similarity: ', sim)
