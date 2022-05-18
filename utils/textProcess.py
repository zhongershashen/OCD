import re
import docx


def docx2string(filename):
    doc = docx.Document(filename)
    article = ''
    for paragraph in doc.paragraphs:
        article += paragraph.text.strip()
    return article


def split_article(query_all):
    query_array = re.split(u"[，；。！？]", query_all)
    if len(query_array[-1]) < 5:
        query_array.pop(-1)
    flag = len(query_array) - 1
    i = -1
    while (i < flag):
        i += 1
        if i > flag - 1:
            break
        elif len(query_array[i]) < 38:
            if len(query_array[i]) + len(query_array[i + 1]) > 38:
                continue
            else:
                query_array[i + 1] = query_array[i] + query_array[i + 1]
                query_array.pop(i)
                flag -= 1
                i -= 1
        else:
            continue
    res = [el.replace('\xa0', ' ') for el in query_array]
    return res
