import sqlite3
from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from App import MyWidget
from functions.post_to_merpyzf import post_to_merpyzf
from functions.save_to_date import ReadAndWriteDate


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.read_write_date = ReadAndWriteDate()
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        self.current_directory = f"{Path.cwd()}/book.db"

        self.resize(800, 600)
        self.setWindowTitle("纸间书摘 PC 书评导入")
        self.setWindowIcon(QIcon("assets/favicon.png"))

        self.ip = ""
        # 隐藏标题栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # 设置自定义标题栏
        toolbar = QToolBar()
        toolbar.setMovable(False)

        self.btn_home = QPushButton(text="", icon=QIcon("assets/home.svg"))
        self.btn_home.clicked.connect(lambda: self.initialize_ui())
        self.btn_author = QPushButton(text="", icon=QIcon("assets/author.svg"))
        self.btn_author.clicked.connect(lambda: self.author_interface())
        self.btn_settings = QPushButton(text="", icon=QIcon("assets/settings.svg"))
        self.btn_home.setFlat(True)
        self.btn_author.setFlat(True)
        self.btn_settings.setFlat(True)

        widget_filling = QWidget()
        toolbar.addWidget(widget_filling)
        layout = QHBoxLayout(widget_filling)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_author)
        layout.addWidget(self.btn_settings)

        self.now_ui = QLabel("主页")
        self.now_ui.setStyleSheet("color:green;font-size:24pt")
        self.now_ip = QLabel(f"当前ip：{self.ip}")

        layout.addWidget(self.now_ui)
        layout.addStretch()
        layout.addWidget(self.now_ip)
        layout.addStretch()

        self.btn_min = QPushButton(text="", icon=QIcon("assets/min.svg"))
        self.btn_max = QPushButton(text="", icon=QIcon("assets/max-normal.svg"))
        btn_close = QPushButton(text="", icon=QIcon("assets/close.svg"))

        self.btn_min.setFlat(True)
        self.btn_max.setFlat(True)
        btn_close.setFlat(True)

        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(btn_close)
        # 最小化、最大化、结束程序
        self.btn_min.clicked.connect(self.showMinimized)
        # 判断当前状态，如果是窗口模式，图片为最大化，功能是最大化；
        # 如果是最大化模式，反之。
        self.btn_max.clicked.connect(lambda: self.window_max())
        btn_close.clicked.connect(self.close)

        self.addToolBar(toolbar)
        toolbar.mouseMoveEvent = self.move_title_bar

        self.initialize_ui()

    def initialize_ui(self):
        self.now_ip.setText(f"当前ip：{self.ip}")
        self.now_ui.setText("主页")
        self.back = QWidget()
        self.setCentralWidget(self.back)
        self.layout = QVBoxLayout()

        self.ip_text = QLineEdit()
        self.ip_text.setText(f"{self.ip}")

        self.back.setLayout(self.layout)

        w = QWidget()
        form = QFormLayout()
        w.setLayout(form)

        form.addRow(QLabel("ip地址"), self.ip_text)

        self.layout.addWidget(w)
        # 上面的是第一行，ip地址，下面写的是已经填写过的书，储存在一个数据库中，可以删除

        # 读取数据库，打开图书表

        conn = sqlite3.connect(self.current_directory)
        c = conn.cursor()
        c.execute("SELECT * FROM book_list bl")

        books = (
            c.fetchall()
        )  # [(1, '老人与海', '2024-10-31'), (2, '阿长与山海经', '2024-10-31')]
        conn.close()

        # 把读取到的书籍列表
        books_widget = QWidget()
        bw_layout = QVBoxLayout()
        books_widget.setLayout(bw_layout)
        self.ip_text.setFocus()

        area = QScrollArea()
        area.setWidgetResizable(True)
        for book in books:
            widget_book = QWidget()
            layout_book = QHBoxLayout(widget_book)
            book_name = QPushButton(f"{book[1]}")

            book_name.clicked.connect(lambda _, x=book[1]: self.open_book_note(x))

            remove_book = QPushButton(text="", icon=QIcon("assets/remove.svg"))
            remove_book.setFlat(True)
            remove_book.clicked.connect(lambda _, x=book[1]: self.ok_ok(x))

            layout_book.addWidget(book_name, 1)
            layout_book.addWidget(remove_book, 0)

            bw_layout.addWidget(widget_book)

        area.setWidget(books_widget)
        self.layout.addWidget(area)

        self.layout.addStretch()
        open_write_info = QPushButton("记录新书")
        open_write_info.clicked.connect(lambda: self.add_new_book())
        self.layout.addWidget(open_write_info)

    def author_interface(self):
        self.now_ui.setText("作者信息")
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel(f"<span style='font-size:24pt'>作者简介</span>"))
        label_0 = QLabel(
            "Hello ，这里是<a href='https://childeyouyu.github.io/'>公子有语</a>，语书摘的开发者。"
        )
        label_0.setOpenExternalLinks(True)
        layout.addWidget(label_0)
        label_1 = QLabel(
            "语书摘是一款专门为纸间书摘开发的第三方app，用于在Windows上进行书摘记录，并提供通过api导入到手机功能的程序。"
        )
        label_1.setWordWrap(True)
        layout.addWidget(label_1)
        layout.addWidget(QLabel("本程序使用 Python、PySide6开发而成。"))

        label_2 = QLabel(
            "如果程序对你有帮助，欢迎您的捐助或 <a href='https://github.com/childeyouyu/merpyzf_pyside6'>Star</a>"
        )
        label_2.setOpenExternalLinks(True)
        layout.addWidget(label_2)

        label_3 = QLabel()
        pixmap = QPixmap("assets/公子有语.png")
        # 缩放图片到新的尺寸
        scaled_pixmap = pixmap.scaled(
            300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )  # 设置新的尺寸为100x100
        label_3.setPixmap(scaled_pixmap)
        label_3.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_3)

        self.setCentralWidget(widget)

    def add_new_book(self):

        # 顶部的修改ip按钮
        ip_new_and_return_button = self.ip_new_and_return_button()
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(ip_new_and_return_button[1])
        # 书籍信息填写界面
        layout.addWidget(MyWidget())

        self.setCentralWidget(widget)
        ip_new_and_return_button[0].setFocus()

    def ip_new_and_return_button(self):
        self.ip = self.ip_text.text()
        widget = QWidget()
        layout = QHBoxLayout(widget)

        ip_line = QLineEdit()
        ip_line.setText(f"{self.ip}")
        change_ip_button = QPushButton("修改 ip")
        return_button = QPushButton(f"返回菜单   当前 ip：{self.ip}")

        def ip_change():
            self.ip = ip_line.text()
            return_button.setText(f"返回菜单   当前 ip：{self.ip}")

        change_ip_button.clicked.connect(lambda: ip_change())

        return_button.clicked.connect(lambda: self.initialize_ui())

        layout.addWidget(ip_line)
        layout.addWidget(change_ip_button)
        layout.addWidget(return_button)

        return ip_line, widget

    def ok_ok(self, book_name):
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle(f"二次确定")
        self.dlg.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f"你确认要删除图书{book_name}吗？"))

        affirm = QPushButton("确认")
        affirm.clicked.connect(lambda _, x=book_name: self.remove_book(x))
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.dlg.close)
        layout.addWidget(affirm)
        layout.addWidget(cancel)

        self.dlg.setLayout(layout)

        self.dlg.exec()

    def window_max(self):
        if self.isMaximized():
            self.showNormal()
            self.btn_max.setIcon(QIcon("assets/max-normal.svg"))
        else:
            self.showMaximized()
            self.btn_max.setIcon(QIcon("assets/max-max.svg"))

        self.btn_max.clearFocus()

    def move_title_bar(self, event):
        """
        拖动顶部标题条
        :param event:
        :return:
        """
        self.windowHandle().startSystemMove()

    def remove_book(self, book_name):
        conn = sqlite3.connect(self.current_directory)
        c = conn.cursor()
        c.execute("DELETE FROM book_list WHERE book_name = ?", (book_name,))
        conn.commit()
        conn.close()
        self.initialize_ui()
        self.dlg.close()
        print(book_name)

    def add_note_interface(self, book_name, text="", note=""):
        widget = QWidget()
        layout = QFormLayout(widget)

        submit_note_or_not_checkbox = QCheckBox("同时提交书摘到纸间书摘")
        layout.addWidget(submit_note_or_not_checkbox)

        text = QTextEdit(text)
        note = QTextEdit(note)
        layout.addRow(QLabel("原文"), text)
        layout.addRow(QLabel("想法"), note)

        h_widget = QWidget()
        h_widget_layout = QHBoxLayout(h_widget)

        btn_add_return = QPushButton("提交并返回")
        btn_add_return.clicked.connect(
            lambda: self.btn_add_note(
                book_name, text.toPlainText(), note.toPlainText(), True
            )
        )

        btn_add_just = QPushButton("提交但不返回")

        btn_add_just.clicked.connect(
            lambda: self.btn_add_note(
                book_name,
                text.toPlainText(),
                note.toPlainText(),
            )
        )

        h_widget_layout.addWidget(btn_add_return)
        h_widget_layout.addWidget(btn_add_just)

        layout.addWidget(h_widget)

        self.setCentralWidget(widget)

    def btn_add_note(self, book_name, text="", note="", state=False):
        if text == "" and note == "":
            # 如果没有书摘，就不要记录
            return
        self.read_write_date.get_book_id(book_name)
        self.read_write_date.insert_note(text, note)
        if state:
            self.initialize_ui()

    def open_book_note(self, book_name):
        # [(1, '话说天下大势，分久必合合久必分。', '开篇立意，表明全书主旨。', 'no_send', '2024-11-04 21:01:04'),
        #  (2, '话说天下大势，分久必合合久必分。', '开篇立意，表明全书主旨。', 'no_send', '2024-11-04 21:02:53'),
        #  (3, '最终三国归晋，这天下又回归一统。', '回应开头的分久必合合久必分。', 'no_send', '2024-11-04 21:14:54')]
        self.read_write_date.get_book_id(book_name)
        note_list = self.read_write_date.get_note_list()
        self.book_name = book_name

        widget_all = QWidget()  # 最大的整块，里面放一个列布局
        layout = QVBoxLayout(widget_all)
        # 列布局第一行：行布局：当前ip：edit line，修改ip：button
        widget_first = self.ip_new_and_return_button()
        layout.addWidget(widget_first[1])

        # 第二行：书名，字体大一点右侧加按钮
        book_name_label = QLabel(
            f"<span style='font-size:16pt'>{book_name}</span>"
            # f"<span style='font-size:16pt; color:#FF0000;'>{book_name}</span>"
        )
        book_name_label.setWordWrap(True)
        book_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(book_name_label)
        # book_name_label.setStyleSheet("QLabel { color: red; background-color: green; }")

        # 第三行，显示书摘
        # widget_second = QWidget()
        # layout_second = QHBoxLayout(widget_second)

        # 左侧：滚动的列布局，居中显示，里面放很多的小widget，内容是：原文+书摘，
        area = QScrollArea()
        widget_area = QWidget()
        # widget_area.setStyleSheet("background-color: rgb(255, 255, 255);")
        area.setWidgetResizable(True)
        # area.setStyleSheet("background-color: rgb(255, 255, 255);")
        # area.setWidget(widget_area)
        # widget_right = QWidget()
        # layout_second.addWidget(widget_left)
        # layout_second.addWidget(widget_right)
        layout_area = QVBoxLayout(widget_area)
        layout_area.addStretch(1)
        # layout.addLayout(layout_area)
        # layout_row = QHBoxLayout(widget_left)
        # layout_row.setStretch(0, 1)

        # widget_child = QWidget()
        # layout_area = QVBoxLayout(widget_child)

        # for r in range(15):
        for i in note_list:
            text = QLabel(i[1])
            note = QLabel(i[2])
            # layout_area.addWidget(zw)
            layout_area.addWidget(
                text
                # , alignment=Qt.AlignmentFlag.AlignCenter
            )
            # 设置一个分割线
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.HLine)  # 设置为水平分割线
            frame.setLineWidth(1)  # 设置分割线宽度为1像素
            layout_area.addWidget(frame)
            layout_area.addWidget(note)

            text.setAlignment(Qt.AlignCenter)
            note.setAlignment(Qt.AlignCenter)

            text.setWordWrap(True)
            note.setWordWrap(True)

            widget_control_book = QWidget()
            layout_control_book = QHBoxLayout(widget_control_book)

            change_note_btn = QPushButton("修改书摘")
            remove_note_btn = QPushButton(icon=QIcon("assets/remove.svg"))  # 删除书摘
            # remove_note_btn.setFlat(True)

            layout_control_book.addWidget(change_note_btn)
            layout_control_book.addWidget(remove_note_btn)

            layout_area.addWidget(widget_control_book)
            # layout_area.addWidget(QPushButton("删除书摘"))
            # zw.setWordWrap(True)

            # text.setStyleSheet("QLabel { width: 100%;font-size:20pt; }")
            # note.setStyleSheet("QLabel { width: 100%;font-size:20pt; }")

        # 右侧:写新书摘按钮和提交书摘到手机按钮
        widget_right = QWidget()
        layout_right = QVBoxLayout(widget_right)
        write_note_button = QPushButton("增加书摘")
        write_note_button.clicked.connect(
            lambda _, x=book_name: self.add_note_interface(x)
        )
        submit_to_phone_button = QPushButton("提交到手机")
        submit_to_phone_button.clicked.connect(lambda: self.submit_to_phone())

        layout_right.addWidget(write_note_button)
        layout_right.addWidget(submit_to_phone_button)

        widget_area.update()
        area.setWidget(widget_area)
        layout.addWidget(area)
        layout.addWidget(widget_right)

        self.setCentralWidget(widget_all)
        widget_first[0].setFocus()
        ...

    def submit_to_phone(self):
        # 获取书摘列表
        book_name = self.book_name
        self.read_write_date.get_book_id(book_name)
        no_send_notes = self.read_write_date.get_notes()
        for note in no_send_notes:
            line = [note[1], note[2]]
            print(self.ip)
            post_to_merpyzf(line, book_name, self.ip)

        pass
