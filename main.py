import csv
import json
import os

import requests
from PySide6 import QtWidgets
import sys

from PySide6.QtWidgets import QHBoxLayout, QFileDialog
from qt_material import apply_stylesheet


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()

        self.QWidget = QtWidgets.QWidget()
        self.layout.addWidget(self.QWidget)

        # 左侧布局：原文及摘录
        lay_left = QtWidgets.QFormLayout()
        self.QWidget.setLayout(lay_left)

        self.line_edit = QtWidgets.QTextEdit()
        self.book_extracts_edit = QtWidgets.QTextEdit()

        lay_left.addRow("原文摘录", self.line_edit)
        lay_left.addRow("书摘", self.book_extracts_edit)

        # 右侧部件，乱七八糟的和提交按钮
        self.RQWidget = QtWidgets.QWidget()
        self.layout.addWidget(self.RQWidget)

        lay_right = QtWidgets.QFormLayout()
        self.RQWidget.setLayout(lay_right)

        self.ip_edit = QtWidgets.QLineEdit()
        self.title_edit = QtWidgets.QLineEdit()
        self.author_edit = QtWidgets.QLineEdit()
        self.translator_edit = QtWidgets.QLineEdit()
        self.publisher_edit = QtWidgets.QLineEdit()
        self.isbn_edit = QtWidgets.QLineEdit()

        # 创建一个调色板并设置文本颜色为红色
        self.ip_edit.setStyleSheet("color: green")
        self.title_edit.setStyleSheet("color: green")
        self.author_edit.setStyleSheet("color: green")
        self.translator_edit.setStyleSheet("color: green")
        self.publisher_edit.setStyleSheet("color: green")

        lay_right.addRow("ip", self.ip_edit)
        lay_right.addRow("书名", self.title_edit)
        lay_right.addRow("作者", self.author_edit)
        lay_right.addRow("译者", self.translator_edit)
        lay_right.addRow("出版社", self.publisher_edit)
        lay_right.addRow("图书 ISBN", self.isbn_edit)
        self.submit_btn = QtWidgets.QPushButton("提交")
        self.submit_btn.clicked.connect(self.button_clicked)
        lay_right.addRow(self.submit_btn)
        # self.layout.addWidget(line_edit)

        # 添加一些其他的功能
        self.OQWidget = QtWidgets.QWidget()
        self.layout.addWidget(self.OQWidget)
        lay_other = QtWidgets.QFormLayout()
        self.OQWidget.setLayout(lay_other)

        self.file_to_merpyzf_btn = QtWidgets.QPushButton("将文件导入到纸间书摘")
        self.file_to_merpyzf_btn.clicked.connect(self.file_to_merpyzf_btn_clicked)

        lay_other.addRow(self.file_to_merpyzf_btn)

        self.setLayout(self.layout)

    def button_clicked(self):
        # 获取输入
        ip = self.ip_edit.text()  # 获取 ip 输入
        title = self.title_edit.text()  # 获取书名输入
        author = self.author_edit.text()  # 获取作者输入
        translator = self.translator_edit.text()  # 获取译者输入
        publisher = self.publisher_edit.text()  # 获取出版社输入
        isbn = self.isbn_edit.text()  # 获取 ISBN 输入
        text = self.line_edit.toPlainText()  # 获取原文输入
        note = self.book_extracts_edit.toPlainText()  # 获取笔记输入

        if ip == "":
            QtWidgets.QMessageBox.information(self, "提示", "找不到你滴 ip 呀！")
            return
        elif title == "":
            QtWidgets.QMessageBox.information(self, "提示", "书名不能为空哦！")
            return
        elif text == "":
            QtWidgets.QMessageBox.information(self, "提示", "没有原文去哪写书评！")
            return

        def submit_note(self):
            # 构造数据
            data = {
                "title": title,  # 书名：必填
                # "cover": "https:#img2.doubanio.com/view/subject/l/public/s29707472.jpg",  # 书籍封面：选填
                "author": author,  # 作者：选填
                "translator": translator,  # 译者：选填
                "publisher": publisher,  # 出版社：选填
                # "publishDate": 1519833600,  # 出版日期：单位秒，选填
                "isbn": isbn,  # ISBN：选填
                "type": 1,  # 书籍类型，必填。可取值：0：纸质书；1：电子书
                "locationUnit": 1,  # 书籍页码类型，必填。可取值：0：进度；1：位置；2：页码
                "entries": [{"text": text, "note": note}],
            }

            # 发送请求
            url = "http://" + ip + ":8080/send"  # 构造请求 URL

            headers = {"ContentType": "application/json"}  # 设置请求头

            response = requests.post(
                url, data=json.dumps(data), headers=headers
            )  # 发送 POST 请求

            if response.status_code == 200:  # 判断返回状态码
                print("保存成功！")
                # 弹出提示窗口，显示：保存成功
                QtWidgets.QMessageBox.information(self, "提示", "保存成功！")
                # self.note_text.delete("1.0", "end")  # 清空笔记文本框
            else:
                QtWidgets.QMessageBox.information(self, "提示", "保存失败，检查你填入的内容")
                print("保存失败，请重试")

        submit_note(self)

    def file_to_merpyzf_btn_clicked(self):
        ip = self.ip_edit.text()  # 获取 ip 输入
        if ip == "":
            QtWidgets.QMessageBox.information(self, "提示", "时刻需要 ip 呀！")
            return

        def file_csv_to_merpyzf(file_name):
            """
            传入一个 csv 文件，将 csv 名作为书籍信息进行导入
            :return:
            """
            read_info = []
            # 从 CSV 文件中读取数据
            with open(file_name, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    read_info.append(row)  # 打印每一行数据
            return read_info

        def post_to_merpyzf(data, name):
            for line in data:
                print(line)
                note_data = {
                    "title": name,  # 书名：必填
                    "cover": "https:#img2.doubanio.com/view/subject/l/public/s29707472.jpg",  # 书籍封面：选填
                    "author": "author",  # 作者：选填
                    "translator": "translator",  # 译者：选填
                    "publisher": "publisher",  # 出版社：选填
                    "publishDate": 1519833600,  # 出版日期：单位秒，选填
                    # "isbn": "978752175575",  # ISBN：选填
                    "type": 1,  # 书籍类型，必填。可取值：0：纸质书；1：电子书
                    "locationUnit": 0,  # 书籍页码类型，必填。可取值：0：进度；1：位置；2：页码
                    "entries": [
                        {
                            "text": line["原文摘录"],
                            "note": line["想法"],
                            "chapter": line["章节名"],
                            "page": line["进度"],
                            "timestamp": line["笔记创建的时间"],
                        }
                    ],
                }
                print(json.dumps(note_data))
                url = f"http://{ip}:8080/send"
                headers = {"ContentType": "application/json"}  # 设置请求头
                response = requests.post(
                    url,
                    data=json.dumps(note_data),
                    headers=headers,
                )  # 发送 POST 请求

                if response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "提示", "保存成功！")
                else:
                    QtWidgets.QMessageBox.information(
                        self, "提示", "保存失败，向开发者反馈一下吧。" "邮箱：youyu273@foxmail.com"
                    )

        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择文件", "", "All Files (*.csv)"
        )
        print(file_path)
        data = file_csv_to_merpyzf(file_path)
        book_name = os.path.basename(file_path)
        print(book_name)
        book_name = book_name[:-4]

        post_to_merpyzf(data, book_name)


class csv_to_merpyzf:
    def __init__(self):
        self.csv_file = ""
        with open("merpyzf.csv", "r", encoding="utf-8") as f:
            info = f.readlines()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # 设置样式表
    apply_stylesheet(app, theme="dark_teal.xml")
    # 标题
    app.setApplicationName("纸间书摘 PC 书评导入")

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
