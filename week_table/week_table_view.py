from PyQt6.QtWidgets import QTableView, QHeaderView


class WeekTableView(QTableView):
    def __init__(self):
        super().__init__()
        # удаляем вертикальный заголовок
        self.verticalHeader().hide()
        # равномерно заполняем таблицу
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setStretchLastSection(True)

        self.setStyleSheet("QHeaderView::section { background-color:blue }")