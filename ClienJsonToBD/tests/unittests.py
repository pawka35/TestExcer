"""
Автотесты приложения ClientJsonToBD
"""

import unittest
from ClienJsonToBD.main import MainClass
# from db.DBWork import WorkWithBD as WkBD
from db.NotOrm_DBWork import WorkWithBD as WkBD



# тесты для методов класса файла main.py
class TestMainClass(unittest.TestCase):
    # запрос информации по корректному адресу
    def test_correct_url(self):
        main_class = MainClass('http://jsonplaceholder.typicode.com/users')
        response = main_class._get_json_data()
        self.assertEqual(response.status_code, 200)

    # запрос информации по несуществующему адресу
    def test_incorrect_url(self):
        main_class = MainClass('http://jsonplaceholder.typicode.com/users3')
        response = main_class._get_json_data()
        self.assertEqual(response.status_code, 404)

    # корректность разбора json ответа
    def test_json_parser(self):
        main_class = MainClass('http://jsonplaceholder.typicode.com/users')
        response = main_class._get_json_data()
        parsed = main_class._parse_json(response)
        for row in parsed:
            self.assertIs(type(row['id']), int)

    # разбор неккоретного json ответа
    def test_incorrect_json_parser(self):
        main_class = MainClass('http://pawka.ru')
        response = main_class._get_json_data()
        self.assertRaises(Exception, main_class._parse_json, response)

    # чтение файла настроек
    def test_read_ini_file(self):
        self.assertIsNotNone(MainClass.read_ini())


# тесты для класса работы с БД (файл \db\DBWork.py)
class TestDBClass(unittest.TestCase):
    # БД существует
    def test_bd_exists(self):
        sql_file = MainClass.read_ini()
        self.assertTrue(WkBD._check_exists_db(sql_file))

    # БД не существует (новая не должна создаваться)
    def test_bd_not_exists(self):
        sql_file = MainClass.read_ini() + '_not_ex'
        self.assertRaises(FileExistsError, WkBD._check_exists_db, sql_file)

    # вспомогательная функция создания временной таблицы для тестов
    def __create_table(self, table):
        class Test:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return 'Test'

        self.user = Test('Petr')
        self.bd = WkBD(MainClass.read_ini())

        self.bd.cursor.execute(f'create table IF NOT EXISTS {table} (id integer PRIMARY KEY, name text);')
        self.bd.cursor.execute(f"insert into {table} (name) values ('Petr')")
        self.bd.commit_session()

    # вспомогательная функция удаления временной таблицы для тестов
    def __drop_table(self, table):
        self.bd.cursor.execute(f'DROP TABLE {table};')
        self.bd.commit_session()

    #  ищем в БД пользователя который там есть
    def test_correct_find_user(self):
        self.__create_table('Test')
        self.assertEqual(self.bd._WorkWithBD__find_select(self.user).fetchall()[0][0], 1)
        self.__drop_table('Test')

    #  ищем в БД пользователя которого там нет
    def test_incorrect_find_user(self):
        self.__create_table('Test')
        self.user.name = 'Viktor'
        self.assertEqual(len(self.bd._WorkWithBD__find_select(self.user).fetchall()), 0)
        self.__drop_table('Test')

    # пытаемся добавить в БД пользователя повторно
    def test_user_always_in_db(self):
        self.__create_table('Test')
        self.user.name = 'Petr'
        self.assertEqual(self.bd._WorkWithBD__check_result(self.bd._WorkWithBD__find_select(self.user),
                                                           self.user), 1)
        self.__drop_table('Test')

    # пытаемся добавить в БД пользователя, которого там нет
    def test_user_not_in_db_need_add(self):
        self.__create_table('Test')
        self.user.name = 'Liza'
        self.assertEqual(self.bd._WorkWithBD__check_result(self.bd._WorkWithBD__find_select(self.user),                                       self.user), 2)
        self.__drop_table('Test')


if __name__ == '__main__':
    unittest.main()
