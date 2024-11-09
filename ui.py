import sqlite3
from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from App import MyWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # self.current_directory = f"{Path.cwd()}/../book.db"
        self.current_directory = f"{Path.cwd()}/book.db"
        print(f"{Path.cwd()}/book.db")
        print(f"{Path.cwd()}/../book.db")
        self.resize(800, 600)
        self.setWindowTitle("纸间书摘 PC 书评导入")
        self.ip = ""
        # 隐藏标题栏
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        toolbar = QToolBar()
        toolbar.setMovable(False)

        btn_open = QWidget()
        toolbar.addWidget(btn_open)
        layout = QHBoxLayout()
        layout.addStretch()
        btn_open.setLayout(layout)

        btn_min = QPushButton(icon=QIcon("assets/min.svg"))
        btn_max = QPushButton(icon=QIcon("assets/icon-max.svg"))
        btn_close = QPushButton(icon=QIcon("assets/close.svg"))

        layout.addWidget(btn_min)
        layout.addWidget(btn_max)
        layout.addWidget(btn_close)
        # toolbar.addWidget(btn_min)
        # toolbar.addWidget(btn_max)
        # toolbar.addWidget(btn_close)
        # 最小化、最大化、结束程序
        btn_min.clicked.connect(self.showMinimized)

        # 判断当前状态，如果是窗口模式，图片为最大化，功能是最大化；
        # 如果是最大化模式，反之。
        btn_max.clicked.connect(lambda: self.window_max())
        btn_close.clicked.connect(self.close)

        self.addToolBar(toolbar)

        self.initialize_ui()

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标
        if event.button() == Qt.LeftButton:
            self._move_drag = True
            self.cursor_win_pos = event.globalPosition() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        # 移动事件
        if Qt.LeftButton and self._move_drag:
            m_Point = event.globalPosition() - self.cursor_win_pos
            self.move(m_Point.x(), m_Point.y())
            event.accept()

    def mouseReleaseEvent(self, event):  # 鼠标按键释放时,取消移动
        self._move_drag = False

    def window_max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # def mousePressEvent(self, event: QtGui.QMouseEvent):
    #     if event.button() == Qt.LeftButton:
    #         print("点击了鼠标左键")
    #
    # def mouseMoveEvent(self, event: QtGui.QMouseEvent):
    #     print(f"鼠标移动  x:{event.x()} y:{event.y()}")
    #
    # def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
    #     if event.button() == Qt.LeftButton:
    #         print("释放了鼠标左键")

    def move_title_bar(self, event):
        """
        拖动顶部标题条
        :param event:
        :return:
        """
        self.windowHandle().startSystemMove()

    def initialize_ui(self):
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
        # 上面的是第一行，ip地址，下面写的是已经甜家国的书，储存在一个数据库中，可以删除

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
        bw_layout = QFormLayout()
        books_widget.setLayout(bw_layout)

        for book in books:
            book_name = QPushButton(f"{book[1]}")
            book_name.clicked.connect(lambda _, x=book[1]: self.open_book_note(x))

            book_id = QPushButton(f"删除图书")
            book_id.clicked.connect(lambda _, x=book[1]: self.ok_ok(x))
            bw_layout.addRow(book_name, book_id)

        self.layout.addWidget(books_widget)

        self.layout.addStretch()
        open_write_info = QPushButton("记录新书")
        open_write_info.clicked.connect(lambda: self.open_write_info())
        self.layout.addWidget(open_write_info)

    def open_write_info(self):

        self.ip = self.ip_text.text()

        print(self.ip)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        return_button = QPushButton(f"返回菜单   当前 ip：{self.ip}")
        return_button.clicked.connect(lambda: self.initialize_ui())
        layout.addWidget(return_button)
        layout.addWidget(MyWidget(self.ip))
        self.setCentralWidget(widget)

    def ok_ok(self, book_name):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"二次确定")

        layout = QFormLayout()
        layout.addWidget(QLabel(f"你确认要删除图书{book_name}吗？"))

        affirm = QPushButton("确认")
        affirm.clicked.connect(lambda _, x=book_name: self.remove_book(x))
        cancel = QPushButton("取消")
        cancel.clicked.connect(dlg.close)
        layout.addRow(affirm, cancel)

        dlg.setLayout(layout)

        dlg.exec()

    def remove_book(self, book_name):
        conn = sqlite3.connect(self.current_directory)
        c = conn.cursor()
        c.execute("DELETE FROM book_list WHERE book_name = ?", (book_name,))
        conn.commit()
        conn.close()
        self.initialize_ui()
        print(book_name)

    def open_book_note(self, book_name):
        select_note_sql = f"SELECT * FROM {book_name}"
        conn = sqlite3.connect(self.current_directory)
        # [(1, '话说天下大势，分久必合合久必分。', '开篇立意，表明全书主旨。', 'no_send', '2024-11-04 21:01:04'),
        #  (2, '话说天下大势，分久必合合久必分。', '开篇立意，表明全书主旨。', 'no_send', '2024-11-04 21:02:53'),
        #  (3, '最终三国归晋，这天下又回归一统。', '回应开头的分久必合合久必分。', 'no_send', '2024-11-04 21:14:54')]
        c = conn.cursor()
        c.execute(select_note_sql)
        note_list = c.fetchall()
        print(c.fetchall())
        conn.close()

        widget_all = QWidget()  # 最大的整块，里面放一个列布局
        layout = QVBoxLayout(widget_all)
        # 列布局第一行：行布局：当前ip：edit line，修改ip：button
        widget_first = QWidget()
        layout_first = QFormLayout(widget_first)
        ip_line = QLineEdit()
        ip_line.setText(f"{self.ip}")
        change_ip_button = QPushButton("修改 ip")
        layout_first.addRow(ip_line, change_ip_button)

        layout.addWidget(widget_first)

        # 第二行：书名，字体大一点右侧加按钮
        layout.addWidget(QLabel(book_name))
        # 第三行，分成两个列布局
        widget_second = QWidget()
        layout_second = QHBoxLayout(widget_second)

        widget_left = QWidget()
        widget_right = QWidget()
        layout_second.addWidget(widget_left)
        layout_second.addWidget(widget_right)

        layout.addLayout(layout_second)

        # 左侧：滚动的列布局，居中显示，里面放很多的小widget，内容是：原文+书摘，
        area = QScrollArea()

        layout_left = QVBoxLayout(widget_left)

        for r in range(15):
            for i in note_list:
                layout_left.addWidget(QLabel(i[1]))
                layout_left.addWidget(QLabel(i[2]))
                layout_left.addWidget(QPushButton("删除书摘"))
                layout_left.addWidget(QLabel(""))

        area.setWidget(widget_left)
        # 右侧:写新书摘按钮和提交书摘到手机按钮
        layout_right = QVBoxLayout(widget_right)
        write_note_button = QPushButton("增加书摘")
        submit_to_phone_button = QPushButton("提交到手机")

        layout_right.addWidget(write_note_button)
        layout_right.addWidget(submit_to_phone_button)

        layout.addWidget(area)
        layout.addWidget(widget_right)

        self.setCentralWidget(widget_all)
        ...
