import json
import os.path
from threading import Thread
from django.http import HttpResponse
from consts import errno


# Create your views here.
from utils.calculate import get_single_repeat
from utils.textProcess import docx2string, split_article


def async_loop(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def upload(request):
    data = {
        "repeat_ratio": "",
        "len_count": "",
        "repeat_count": "",
        "list": []
    }
    ret = {'code': '', "data": ''}
    file = request.data.get('file')
    file_path = 'files'
    file_name = os.path.join(file_path,file.name)
    repeat_count = 0
    len_count = 0
    with open(file_name, "wb") as f:
        # 写入字节流
        f.write(file.file.read())

    querylist = split_article(docx2string(file_name))

    for keyword in querylist:
        temp_dic = get_single_repeat(keyword)
        data['list'].append(temp_dic)
        repeat_count += temp_dic['repeat_ratio'] * len(keyword)
        len_count += len(keyword)

    repeat_ratio = repeat_count / len_count

    data['repeat_ratio'] = repeat_ratio
    data['repeat_count'] = repeat_count
    data['len_count'] = len_count

    ret['code'] = errno.SUCCESS_NO
    ret['data'] = data

    # 返回响应
    return HttpResponse(content=json.dumps(ret), content_type="application/json")
