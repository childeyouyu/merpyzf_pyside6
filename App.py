import os
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog

from functions import file_csv_to_merpyzf, post_to_merpyzf
from functions.save_to_date import ReadAndWriteDate


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # self.layout = QHBoxLayout()
        self.read_write_date = ReadAndWriteDate()

        self.QWidget = QtWidgets.QWidget()
        # self.layout.addWidget(self.QWidget)

        # 右侧部件，乱七八糟的和提交按钮

        layout = QtWidgets.QFormLayout(self)
        # self.QWidget.setLayout(lay_right)

        # self.ip_edit = QtWidgets.QLineEdit()
        self.title_edit = QtWidgets.QLineEdit()
        self.cover = QtWidgets.QLineEdit()
        self.author_edit = QtWidgets.QLineEdit()
        self.translator_edit = QtWidgets.QLineEdit()
        self.publisher_edit = QtWidgets.QLineEdit()
        self.isbn_edit = QtWidgets.QLineEdit()
        self.boot_introduction = QtWidgets.QTextEdit()

        # 创建一个调色板并设置文本颜色为绿色
        # self.ip_edit.setStyleSheet("color: green")
        self.title_edit.setStyleSheet("color: green")
        self.author_edit.setStyleSheet("color: green")
        self.translator_edit.setStyleSheet("color: green")
        self.publisher_edit.setStyleSheet("color: green")

        # lay_right.addRow("ip", self.ip_edit)
        layout.addRow("书名", self.title_edit)
        layout.addRow("作者", self.author_edit)
        layout.addRow("译者", self.translator_edit)
        layout.addRow("出版社", self.publisher_edit)
        layout.addRow("图书 ISBN", self.isbn_edit)
        layout.addRow("图书简介", self.boot_introduction)

        # 创建QFrame
        frame = QtWidgets.QFrame(self)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # 设置尺寸策略为自动扩充
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        frame.setSizePolicy(sizePolicy)
        frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        # 设置QFrame背景为透明
        frame.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        layout.addWidget(frame)
        self.submit_btn = QtWidgets.QPushButton("提交")
        self.submit_btn.clicked.connect(self.button_clicked)
        layout.addRow(self.submit_btn)

        # self.setLayout(layout)

    def button_clicked(self):
        # 获取输入
        # ip = self.ip  # 获取 ip 输入
        title = self.title_edit.text()  # 获取书名输入
        # cover = self.cover.text()
        author = self.author_edit.text()  # 获取作者输入
        translator = self.translator_edit.text()  # 获取译者输入
        publisher = self.publisher_edit.text()  # 获取出版社输入
        isbn = self.isbn_edit.text()  # 获取 ISBN 输入
        book_introduction = self.boot_introduction.toPlainText()
        # text = self.line_edit.toPlainText()  # 获取原文输入
        # note = self.book_extracts_edit.toPlainText()  # 获取笔记输入

        # if self.ip == "":
        #     QtWidgets.QMessageBox.information(self, "提示", "找不到你滴 ip 呀！")
        #     return
        if title == "":
            QtWidgets.QMessageBox.information(self, "提示", "书名不能为空哦！")
            return
        self.read_write_date.save_book(title, author, translator, publisher, isbn, book_introduction)
        # elif text == "":
        #     QtWidgets.QMessageBox.information(self, "提示", "没有原文去哪写书评！")
        #     return

        # status_code = submit_note(
        #     ip,
        #     {
        #         "title": title,
        #         "cover": cover,
        #         "author": author,
        #         "translator": translator,
        #         "publisher": publisher,
        #         "isbn": isbn,
        #     },
        #     text,
        #     note,
        # )

        # check status code and display output
        # if status_code == 200:  # 判断返回状态码
        #     print("保存成功！")
        #     # 弹出提示窗口，显示：保存成功
        #     QtWidgets.QMessageBox.information(self, "提示", "保存成功！")
        #     # self.note_text.delete("1.0", "end")  # 清空笔记文本框
        # else:
        #     QtWidgets.QMessageBox.information(
        #         self, "提示", "保存失败，检查你填入的内容"
        #     )
        #     print("保存失败，请重试")

    def file_to_merpyzf_btn_clicked(self):
        ip = self.ip_edit.text()  # 获取 ip 输入
        if ip == "":
            QtWidgets.QMessageBox.information(self, "提示", "时刻需要 ip 呀！")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择文件", "", "All Files (*.csv)"
        )

        print(file_path)

        data = file_csv_to_merpyzf(file_path)

        data = file_csv_to_merpyzf(file_path)
        book_name = os.path.basename(file_path)
        print(book_name)
        book_name = book_name[:-4]

        for line in data:
            status_code = post_to_merpyzf(line, book_name, ip)
            if status_code == 200:
                QtWidgets.QMessageBox.information(self, "提示", "保存成功！")
            else:
                QtWidgets.QMessageBox.information(
                    self,
                    "提示",
                    "保存失败，向开发者反馈一下吧。" "邮箱：youyu273@foxmail.com",
                )
