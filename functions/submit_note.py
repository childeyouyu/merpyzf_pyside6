import requests
import json


def submit_note(ip: str, book_info: dict, text: str, note: str):
    # 构造数据
    data = {
        "title": book_info["title"],  # 书名：required
        "cove": book_info["cover"],
        # "cover": "https:#img2.doubanio.com/view/subject/l/public/s29707472.jpg",  # 书籍封面：optional
        "author": book_info["author"],  # 作者：optional
        "translator": book_info["translator"],  # 译者：optional
        "publisher": book_info["publisher"],  # 出版社：optional
        # "publishDate": 1519833600,  # 出版日期：单位秒，optional
        "isbn": book_info["isbn"],  # ISBN：optional
        "type": 1,  # 书籍类型，required。可取值：0：纸质书；1：电子书
        "locationUnit": 1,  # 书籍页码类型，required。可取值：0：进度；1：位置；2：页码
        "entries": [{"text": text, "note": note}],
    }

    # 发送请求
    url = "http://" + ip + ":8080/send"  # 构造请求 URL

    headers = {"ContentType": "application/json"}  # 设置请求头

    response = requests.post(
        url, data=json.dumps(data), headers=headers
    )  # 发送 POST 请求

    return response.status_code
