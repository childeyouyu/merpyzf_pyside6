import sys

from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from view.ui import MainWindow


def main():
    app = QApplication(sys.argv)
    # 设置样式表
    apply_stylesheet(app, theme="dark_teal.xml")

    main_windows = MainWindow()
    main_windows.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # logging.debug(PySide6.__version__)

    main()
