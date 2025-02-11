from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt6.QtGui import QColor, QBrush


class WeekTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.columns = 7
        self.rows = 1
        self.headers = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

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
            if index.column() < 5:
                return QBrush(QColor(176, 224, 230))
            else:
                return QBrush(QColor(255, 160, 122))

    def headerData(self, section, orientation, role = ...):

        if role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        super().headerData(section, orientation, role)