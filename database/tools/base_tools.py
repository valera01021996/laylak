from database.utils import connect_database


class BaseTools:
    """Базовый инструмент. Подключение к БД"""
    def __init__(self):
        self.connection, self.cursor = connect_database("database.sqlite")


    def _repeat_connection(self):
        self.__init__()