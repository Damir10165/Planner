import datetime

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QDate
from PyQt6.QtGui import QColor, QBrush


class WeekTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.columns = 7
        self.rows = 1
        # названия дней недели и даты
        self.headers_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.week_dates = ["", "", "", "", "", "", ""]
        self.today = datetime.datetime.today().date().strftime('%d.%m.%Y')

        # цвета соответствеющие дням недели
        self.weekdays_color = QColor(176, 224, 230)
        self.weekend_color = QColor(255, 160, 122)
        self.today_color = QColor(185, 255, 131)
        self.headers_colors = [self.weekdays_color, self.weekdays_color,
                               self.weekdays_color, self.weekdays_color,
                               self.weekdays_color, self.weekend_color, self.weekend_color]

    def parent(self):
        return QModelIndex()

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        return self.rows

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return " "
        if role == Qt.ItemDataRole.BackgroundRole:
            if self.today == self.week_dates[index.column()]:
                return QBrush(self.today_color)
            return QBrush(self.headers_colors[index.column()])

    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            # объединяем названия дней недели и даты
            return self.headers_week[section] + "\n" + self.week_dates[section]

    def update_data(self, selected_day):
        # заполняем список с датами на основе выбранной даты
        for i in range(7):
            self.week_dates[i] = selected_day.addDays(i - selected_day.dayOfWeek() + 1).toString("dd.MM.yyyy")
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, self.columns - 1)
