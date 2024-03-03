from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from qt_material import apply_stylesheet
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("纸间书摘 PC 书评导入")


def main():
    app = QApplication(sys.argv)
    # 设置样式表
    apply_stylesheet(app, theme="dark_teal.xml")
    # 标题
    main_windows = MainWindow()
    main_windows.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
