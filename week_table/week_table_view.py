from PyQt6.QtWidgets import QTableView, QHeaderView
from PyQt6.QtCore import Qt


class WeekTableView(QTableView):
    def __init__(self):
        super().__init__()
        # удаляем вертикальный заголовок
        self.verticalHeader().hide()
        # равномерно заполняем таблицу
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setStretchLastSection(True)

    def keyPressEvent(self, e):
        # удаление данных ячейки при нажатии клавишы DEL
        if e.key() == Qt.Key.Key_Delete:
            self.model().setData(index=self.currentIndex(), value=None, role=Qt.ItemDataRole.DisplayRole)
