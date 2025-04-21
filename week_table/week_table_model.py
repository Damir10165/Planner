import datetime

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QDate
from PyQt6.QtGui import QColor, QBrush

from db.planner_db import PlannerDB


class WeekTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.db = PlannerDB()
        self.db.launch_db()

        self.columns = 7
        self.rows = self.db.get_row()
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
            return self.db.get_data(self.week_dates[index.column()], index.row())
        if role == Qt.ItemDataRole.BackgroundRole:
            if self.today == self.week_dates[index.column()]:
                return QBrush(self.today_color)
            return QBrush(self.headers_colors[index.column()])

    def setData(self, index, value, role=Qt.ItemDataRole.DisplayRole):
        if value is None:
            # удаление данных из ячейки
            self.db.del_data(date=self.week_dates[index.column()], row=index.row())
            new_rows = self.db.get_row()
            self.beginRemoveRows(index.parent(), new_rows, self.rows)
            self.rows = new_rows
            self.endRemoveRows()
        if value:
            if self.db.get_data(date=self.week_dates[index.column()], row=index.row()):
                # изменяем данные в ячейке, в которой уже присутствует запись
                self.db.update_data(date=self.week_dates[index.column()], row=index.row(), text=value)
            else:
                # добавляем новые данные
                self.beginInsertRows(index.parent(), self.rows, self.rows + 1)
                self.db.add_data(date=self.week_dates[index.column()], row=index.row(), text=value)
                self.insertRows(self.rows, 1, index.parent())
                # при добавлении информации в последнюю строку автоматически создается новая строка
                if index.row() == self.rows - 1:
                    self.rows += 1
                    self.db.update_row(self.rows)
                self.endInsertRows()

        # испускаем сигналы об изменении данных
        self.dataChanged.emit(index, index)
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, self.columns - 1)
        return True

    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            # объединяем названия дней недели и даты
            return self.headers_week[section] + "\n" + self.week_dates[section]

    def update_data(self, selected_day):
        # заполняем список с датами на основе выбранной даты
        for i in range(7):
            self.week_dates[i] = selected_day.addDays(i - selected_day.dayOfWeek() + 1).toString("dd.MM.yyyy")
        self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, self.columns - 1)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
