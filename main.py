import sys

from PyQt6.QtWidgets import QApplication

from my_main_window import MyMainWindow


app = QApplication(sys.argv)

mw = MyMainWindow()
mw.show()

sys.exit(app.exec())

