"""
Автотесты приложения ClientJsonToBD
"""

import unittest
from ClienJsonToBD.main import MainClass
#from db.DBWork import WorkWithBD as WkBD
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
        self.assertRaises(Exception,  main_class._parse_json, response)

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
        sql_file = MainClass.read_ini()+'_not_ex'
        self.assertRaises(FileExistsError, WkBD._check_exists_db, sql_file)


if __name__ == '__main__':
    unittest.main()
