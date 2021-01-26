import requests
import sys
from db.DBWork import *
import configparser
sys.path.append('..')


class MainClass:
    def __init__(self, url):
        """
        Коструктор класса MainClass
        :param url: ссылка по которой лежит json
               truncate_tables: предварительно очистить таблицы в БД (по-молчанию: нет)
        """
        self.url = url
        self.db_file = MainClass.read_ini()

    @staticmethod
    def read_ini():
        """
        Получаем путь к файлу БД из файла инициализации
        :return: полный пусть к файлу БД
        """
        config = configparser.ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read(f"{dir_path}/{'client.ini'}")
        return os.path.abspath(os.path.join(os.path.dirname(__file__), config['SETTINGS']['Database_path'],
                                            config['SETTINGS']['Database_file']))

    @staticmethod
    def truncate_tables():
        """
        Статический метод очистки таблиц (со сбросом автоинкремента)
        """
        while True:
            answer = input('Данная процедура уничтожит все данные в БД. Продолжить?[y/n]')
            if answer.casefold() == 'y':
                bd_file = MainClass.read_ini()
                WorkWithBD(bd_file, True)
                break
            elif answer.casefold() == 'n':
                return
            else:
                print('Нет такого варианта ответа')

    def _get_json_data(self):
        """
        Получение данных от сервера
        :return: данные ответа сервера
        """
        try:
            return requests.get(self.url)
        except requests.ConnectionError:
            while True:
                print('Не могу установить соединение с сервером')
                answer = input('Попробовать еще раз? [y/n]')
                if answer == 'n'.casefold():
                    break
                elif answer.casefold() == 'y' or answer.casefold() == 'у':
                    self._get_json_data()
                else:
                    print('Не было такого варианта')
                    self._get_json_data()
            print('Finish program, good bye!')
            exit(0)

    @staticmethod
    def _parse_json(data):
        """
        Парсим данные json в ответе сервера
        :param data: ответ сервера
        :return: json объект, сформированный из данных ответа
        при невозможности разбора выкидываем исключение ValueError
        """
        try:
            res = data.json()
            return res
        except ValueError:
            raise

    def start_work(self):
        """
        Работа основного алгоритма
        :return: если запросили неккоректный адрес - выкидываем исключение NotImplementedError
        """
        req = self._get_json_data()  # получаем ответ от сервера
        if req.status_code == 200:  # если статус ответа 200(ОК) - продолжаем работу
            bd = WorkWithBD(self.db_file)  # создаем экземпляр класса для работы с БД, при необходимости чистим таблицы
            if self.url.endswith('users'):  # если запрос по ссылке, оканчивающейся на users(http://[....]/users)
                for cU in self._parse_json(req):  # для каждого элемента полученного json-объекта
                    bd.new_user_to_bd(cU)  # передаем элемент(строку) для внесение в БД
                bd.commit_session()   # после окончания передачи всех данных в БД фиксируем изменения в БД
            elif self.url.endswith('posts'):  # вышеописанные шаги для ссылки, оканчивающейся на posts
                for cP in self._parse_json(req):
                    bd.new_post_to_bd(cP)
                bd.commit_session()
            else:
                raise NotImplementedError(f'Внесение в БД информации с адреса {self.url} не предусмотрено.')


if __name__ == '__main__':
    MainClass.truncate_tables()  # вызываем процедуру очистки таблиц БД
    users = MainClass('http://jsonplaceholder.typicode.com/users').start_work()  # внесения информации о пользователях
    posts = MainClass('http://jsonplaceholder.typicode.com/posts').start_work()  # внесение информации о постах
