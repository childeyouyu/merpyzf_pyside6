import sqlite3
from pathlib import Path

from functions import save_to_date


def test_save_to_date():
    book_name = "三国演义"
    save_to_date.save_book(book_name)
    save_to_date.insert_note(
        book_name, "最终三国归晋，这天下又回归一统。", "回应开头的分久必合合久必分。"
    )


def test_database():
    try:
        conn = sqlite3.connect("d:/CodeInGitHub/book.db")
        c = conn.cursor()
        c.execute("SELECT * FROM book_list")  # 注意SQL语句中通常使用大写来提高可读性
        items = c.fetchall()
        for item in items:
            print(item)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


def get_path():
    current_directory = Path.cwd()
    print(current_directory)
    ...


import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from PySide6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        toolbar = QToolBar()

        btn_min = QAction()
        btn_min.setIcon(QIcon("assets/min.svg"))
        btn_max = QAction(icon=QIcon("assets/icon-max.svg"))
        btn_close = QAction(icon=QIcon("assets/close.svg"))
        toolbar.addAction(btn_min)
        toolbar.addAction(btn_max)
        toolbar.addAction(btn_close)

        # 最小化、最大化、结束程序
        btn_min.triggered.connect(self.showMinimized)
        btn_max.triggered.connect(self.showMaximized)
        btn_close.triggered.connect(self.close)

        btn_open = QAction("启动")
        toolbar.addAction(btn_open)
        btn_open.triggered.connect(self.on_open_triggered)

        self.addToolBar(toolbar)

        self.setWindowTitle("Custom ToolBar")
        self.resize(400, 300)
        self.show()

    def on_open_triggered(self):
        print("Open action triggered")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())


# if __name__ == "__main__":
#     # test_database()
#     get_path()
