import sys

from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from ui import MainWindow


def main():
    app = QApplication(sys.argv)
    # 设置样式表
    apply_stylesheet(app, theme="dark_teal.xml")
    # # 标题
    # tray_icon = QSystemTrayIcon(QIcon("assets/favicon.png"), app)
    # # 创建托盘菜单
    # menu = QMenu()
    # action = menu.addAction("退出")
    # tray_icon.setContextMenu(menu)
    #
    # # 显示任务栏图标
    # tray_icon.show()

    main_windows = MainWindow()
    main_windows.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
