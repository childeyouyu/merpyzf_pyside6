from PySide6 import QtWidgets
import qt_material
from App import MyWidget
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    # 设置样式表
    qt_material.apply_stylesheet(app, theme="dark_teal.xml")
    # 标题
    app.setApplicationName("纸间书摘 PC 书评导入")

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
