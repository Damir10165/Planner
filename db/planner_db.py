import sqlite3


class PlannerDB:

    def __init__(self):
        self.connection = sqlite3.connect('db/planner_database.db')
        self.cursor = self.connection.cursor()

    def launch_db(self) -> None:
        # создание новой таблицы для дат и записей соответствующих им, если такой нет
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS planner (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                    date TEXT NOT NULL,
                                    row INT NOT NULL,
                                    text TEXT NOT NULL)
                                """)

        # создание таблицы для сохранения количества строк в таблице
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS rows (
                                    row INTEGER NOT NULL DEFAULT 1);
                                """)

        # выставляем количество строк равное 1, если данных о строках нет
        self.cursor.execute("""
                                INSERT INTO rows (row)
                                SELECT 1
                                WHERE 0 = (SELECT COUNT(*) FROM rows)
                                """)
        self.connection.commit()

    def add_data(self, date: str, row: int, text: str) -> None:
        # добавляем новые данные
        self.cursor.execute(f"""
                                INSERT INTO planner (date, row, text)
                                VALUES ('{date}', {row}, '{text}')
                                """)

        self.connection.commit()


    def get_data(self, date: str, row: int) -> str:
        # получаем данные по дате
        cur = self.cursor.execute(f"""SELECT * FROM planner WHERE date = '{date}' AND row = {row}""")
        data = cur.fetchall()

        text = ''
        if data:
            # под 3-им индексом находиться текст
            text = data[0][3]

        return text

    def del_data(self, date: str, row: int) -> None:
        # удаляем данные
        self.cursor.execute(f"""DELETE FROM planner WHERE date = '{date}' AND row = {row}""")
        # удаляем ненужные пустые строки
        max_row = self.cursor.execute("""SELECT MAX(row) FROM planner""").fetchall()[0][0]
        if max_row is None:
            max_row = 0
        self.update_row(max_row + 1)
        self.connection.commit()

    def update_data(self, date: str, row: int, text: str) -> None:
        # обновляем данные
        self.cursor.execute(f"""UPDATE planner SET text = '{text}' WHERE date = '{date}' AND row = {row}""")
        self.connection.commit()

    def update_row(self, row: int) -> None:
        # обновляем количество строк
        self.cursor.execute(f"""UPDATE rows SET row = {row}""")
        self.connection.commit()

    def get_row(self) -> str:
        # возвращаем количество строк
        row = self.cursor.execute(f"""SELECT row FROM rows""").fetchall()
        return row[0][0]


    def __del__(self):
        self.connection.close()
