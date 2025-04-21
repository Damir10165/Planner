from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QCalendarWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from week_table.week_table_model import WeekTableModel
from week_table.week_table_view import WeekTableView


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 200, 1500, 1000)
        self.setWindowTitle("Планинг")
        self.main_layout = QVBoxLayout()

        # кнопка для открытия календаря
        self.btn_calendar = QPushButton()
        self.btn_calendar.setCheckable(True)
        self.btn_calendar.setFixedSize(50, 50)
        self.btn_calendar.setFlat(True)
        self.btn_calendar.setIcon(QIcon("main_window/calenda.png"))
        self.btn_calendar.setIconSize(QSize(45, 45))

        self.calendar = QCalendarWidget()

        # убираем у календаря возможность закрыть его и ставим поверх главного окна
        self.calendar.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.btn_calendar.clicked.connect(self.open_calendar)

        self.main_layout.addWidget(self.btn_calendar, alignment=Qt.AlignmentFlag.AlignRight)
        self.tabel = WeekTableView()
        self.model = WeekTableModel()
        self.tabel.setModel(self.model)
        self.main_layout.addWidget(self.tabel)

        self.update_table()
        self.calendar.selectionChanged.connect(self.update_table)

        wgt = QWidget()
        wgt.setLayout(self.main_layout)
        self.setCentralWidget(wgt)

    def open_calendar(self):
        if self.sender().isChecked():
            # размещаем календарь под кнопкой, которая его открывает
            self.calendar.move(self.x() + self.btn_calendar.x() - 207, self.y() + self.btn_calendar.y()
                               + self.btn_calendar.height() + 30)
            self.calendar.show()
        else:
            self.calendar.close()

    def moveEvent(self, a0):
        super().moveEvent(a0)
        # обновляем расположение календаря при изменении расположения главного окна
        self.calendar.move(self.x() + self.btn_calendar.x() - 207, self.y() + self.btn_calendar.y()
                           + self.btn_calendar.height() + 30)

    def closeEvent(self, a0):
        # закрываем календарь вместе с главным окном
        self.calendar.close()
        super().closeEvent(a0)

    def changeEvent(self, a0):
        super().changeEvent(a0)
        # делаем так, чтобы вовремя сворачивания главного окна, календарь тоже сворачивался
        if a0.type() == a0.type().WindowStateChange:
            self.calendar.setWindowState(self.windowState())
        # поднимаем календарь на самый верх, при взаимодействии с главным окном
        if a0.type() == a0.type().ActivationChange:
            self.calendar.raise_()

    def update_table(self):
        """
            Обновляет состояние таблицы при выборе новой даты в календаре
        """
        self.tabel.model().update_data(self.calendar.selectedDate())
