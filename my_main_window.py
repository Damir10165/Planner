from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QTableView, QWidget, QSizePolicy
from PyQt6.QtCore import Qt


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 200, 1500, 1000)
        self.setWindowTitle("Планинг")

        self.main_layout = QVBoxLayout()

        self.btn_calendar = QPushButton()
        self.btn_calendar.setCheckable(True)
        self.btn_calendar.setFixedSize(30, 30)
        self.main_layout.addWidget(self.btn_calendar, alignment=Qt.AlignmentFlag.AlignRight)
        self.tabel = QTableView()
        self.main_layout.addWidget(self.tabel)

        wgt = QWidget()
        wgt.setLayout(self.main_layout)
        self.setCentralWidget(wgt)