import json

import requests


def post_to_merpyzf(line, name, ip):
    # print(line)
    note_data = {
        "title": name,  # 书名：required
        "cover": "/",  # 书籍封面：optional
        "author": "author",  # 作者：optional
        "translator": "translator",  # 译者：optional
        "publisher": "publisher",  # 出版社：optional
        "publishDate": 1519833600,  # 出版日期：单位秒，optional
        # "isbn": "978752175575",  # ISBN：optional
        "type": 1,  # 书籍类型，required。可取值：0：纸质书；1：电子书
        "locationUnit": 0,  # 书籍页码类型，required。可取值：0：进度；1：位置；2：页码
        "entries": [
            {
                "text": line[0],
                # "text": line["ExcerptFromTheOriginalText"],
                "note": line[1],
                # "note": line["idea"],
                # "chapter": line["chapterName"],
                # "page": line["progress"],
                # "timestamp": line["theTimeWhenTheNoteWasCreated"],
            }
        ],
    }
    # print(json.dumps(note_data))
    url = f"http://{ip}:8080/send"
    headers = {"ContentType": "application/json"}  # 设置请求头
    response = requests.post(
        url,
        data=json.dumps(note_data),
        headers=headers,
    )  # 发送 POST 请求

    return response.status_code
