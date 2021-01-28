from db.NotOrm_Classes import Users, Address, Geo, Company, Posts
import db.NotOrm_Classes as Orm
import inspect
import os
import sqlite3


class WorkWithBD:
    def __init__(self, bd_filename, truncate=False):
        """
        Конструктор класса
        :param bd_filename: полное имя файла базы данных
        :param truncate: флаг необходимости очистки таблиц
        """
        self._check_exists_db(bd_filename)  # процедура проверки существования файла БД (новый не будем создавать)
        self.session = sqlite3.connect(bd_filename)
        self.cursor = self.session.cursor()
        if truncate:  # Если поступила команда на очистку таблиц, то запускаем процедуру
            self.__begin_truncate_tables()

    @staticmethod
    def _check_exists_db(sql_file):
        """
        Проверка существования файла БД, если не существует - выкидываем исключение
        :param sql_file: файл БД (с путем)
        :return: возвращаем истину, в случае сущестования файла
        """
        if not os.path.isfile(sql_file):
            raise FileExistsError('Can`t find db file')
        else:
            return True

    def __del__(self):
        """
        Деструктор класса
        """
        self.session.close()  # закрываем сессию соединения с БД

    def commit_session(self):
        """
        Применяем изменения, которые были в БД
        """
        self.session.commit()

    def __begin_truncate_tables(self):
        """
        Приватный метод (чтобы нельзя бло вызвать на объекте класса), подготавливающий информацию для удаления таблиц
        """
        for name, obj in inspect.getmembers(Orm):  # получаем имена классов из файла OrmClasses.py
            if inspect.isclass(obj):
                self.__truncate_tables(name)  # имя таблицы передаем в метод для ее очистки
        self.session.commit()  # после того, как провели операции над всеми таблицами, фиксируем изменения в БД
        print(f'All tables was truncated')

    def __truncate_tables(self, table):
        """
        Приватный метод очистки таблиц
        Т.к. в sqllite отсуствует оператор truncate (очистка со сбросом значения автоинкремента), делаем руками
        :param table: имя таблицы для очистки
        """
        self.session.execute(f"DELETE FROM {table};")
        self.session.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table}';")
        print(f'Table {table} prepare for truncate')

    def new_post_to_bd(self, post):
        """
        Добавление новой записи в таблице Posts
        :param post: добавляемая запись
        """
        new_post = Posts(post)
        #  ищем в БД пользователя по id, который указан в посте
        find_user = self.cursor.execute(f'select id from Users where id = {new_post.userId};').fetchall()

        if len(find_user) == 0:  # если такого пользователя нет, то пост не добавляем (т.к. неккому привязывать)
            print('No such user!!!')
        else:
            # делаем запрос на выборку из бд строки с аналогичными параметрами поста (кроме id)
            # для исключения случаем повторного занесения информации
            find_post = self.__find_select(new_post)

            self.__check_result(find_post, new_post)  # отправляет результат запроса на обработку

    def new_user_to_bd(self, user):
        """
        Добавление нового пользователя в бд
        :param user: добавляемый пользователь
        """
        # т.к. к таблица пользователя имеет первичные ключи на таблицы company и address, заполним сначала их
        address = self.__add_new_address(user['address'])
        company = self.__add_new_company(user['company'])
        # делаем запрос на выборку из бд строки с аналогичными параметрами пользователя (кроме id)
        # для исключения случаем повторного занесения информации
        user = Users(user)
        user.company = company
        user.address = address
        find_user = self.__find_select(user)

        self.__check_result(find_user, user)  # отправляет результат запроса на обработку

    def __add_new_company(self, company):
        """
        Добавление новой компании в бд
        :param company: данные добавляемой компания
        :return: id добавленной (либо существующей) записи в таблицу
        """
        comp = Company(company)
        # делаем запрос на выборку из бд строки с аналогичными параметрами компании (кроме id)
        # для исключения случаем повторного занесения информации
        result = self.__find_select(comp)

        return self.__check_result(result, comp)  # отправляем результат запроса на обработку

    def __add_new_address(self, address):
        """
        Добавление нового адреса в бд
        :param address: данные добавляемого адреса
        :return: id добавленной (либо существующей) записи в таблицу
        """
        addr = Address(address)
        # т.к. к таблица Address имеет первичный ключ на таблицу Geo(геокоординаты), заполнием сначала её
        addr.geo = self.__add_new_geo(address['geo'])
        result = self.__find_select(addr)
        return self.__check_result(result, addr)  # отправляе результат запроса на обработку

    def __add_new_geo(self, geo):
        """
        Добавление новых координат  в БД
        :param geo - имя пользователя
        :return: id добавленной (либо существующей) записи в таблицу
        """
        geopos = Geo(geo)
        # делаем запрос на выборку из бд строки с аналогичными параметрами координат (кроме id)
        # для исключения случаем повторного занесения информации
        result = self.__find_select(geopos)
        return self.__check_result(result, geopos)  # отправляе результат запроса на обработку

    def __find_select(self, record):
        """
        Формирование запроса для поиска в БД id записи, у которой совпадают с поступившей все параметры (кроме id)
        :param record: запись для поиска в БД
        :return: курсор для поиска
        """
        search_str = []
        for val in record.__dict__:  # переберем все пары ключ:значение полей поступившего объекта
            search_str.append(f"{val}='{record.__dict__[val]}'")  # формируем пары вида "name=val" для SQL запроса
        return self.cursor.execute(f"select id from {str(record)} where {' and '.join(search_str)}")

    def __check_result(self, result, record):
        """
        Обработка результатов запроса существования записи,добавление при необходимости
        :param result: результат запроса
        :param record: запись
        :return: id добавленной или найденой записи
        """
        res_data = result.fetchall()  # получаем все данные из запроса
        if len(res_data) == 0:  # если результат пуст (нет такой записи), то добавляем запись в бд и получаем ее id
            row_names, row_values = [], []  # объявляем пустые списки для сбора ключей и значение объекта
            for val in record.__dict__:  # переберем все пары ключ:значение полей поступившего объекта
                row_names.append(f'{val} ')  # соберем ключи (будут именами полей БД)
                row_values.append(f"'{record.__dict__[val]}'")  # соберем значения (будут значениями полей БД)
            # {str(record)} = мя класса, определяет таблицу для записи
            # {','.join(row_names) - названия полей класса, определяют поле БД таблицы для записи
            # {','.join(row_values)} - значения полей класса, определяют значения соотв. полей БД для записи
            self.cursor.execute(f"INSERT INTO {str(record)}({','.join(row_names)}) values ({','.join(row_values)});")
            row_id = self.cursor.lastrowid
            print(f'{str(record)} id #{row_id} added in bd')

        elif len(res_data) == 1:  # если запись существует в БД, получаем ее id
            print(f'This {str(record)} id #{res_data[0][0]} allready in bd')
            row_id = res_data[0][0]
        else:  # если найдено более чем одна запись - генерируем исключение, т.к. данные доллжны быть уникальны
            raise ValueError(f'Найдено больше 1-ой записи {type(record)}')
        return row_id  # возвращаем id записи
