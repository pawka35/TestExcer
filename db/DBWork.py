from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db.OrmClasses import Users, Address, Geo, Company, Posts
import db.OrmClasses as Orm
import inspect
import os
import re

Base = declarative_base()


class WorkWithBD:
    def __init__(self, bd_filename, truncate=False):
        """
        Конструктор класса
        :param bd_filename: полное имя файла базы данных
        :param truncate: флаг необходимости очистки таблиц
        """
        self._check_exists_db(bd_filename)  # процедура проверки существования файла БД (новый не будем создавать)
        self.metadata = MetaData()  # Создаём объект MetaData
        self.engine = create_engine(f'sqlite:///{bd_filename}', echo=False, pool_recycle=7200)
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()  # сохраняем сессию для использования в методах класса
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
                if 'OrmClasses' in str(obj):  # т.к. используем SQLAlchemy, берем только созданные нами классы
                    m = re.search(r'\.([^.]*)\'', str(obj))  # вычленяем имя класса (соответсвует имени таблицы)
                    self.__truncate_tables(m.group(1))  # имя таблицы передаем в метод для ее очистки
                    # можно и так передать, но тогда Вы не увидите,как я умею работать с регулярками
                    # self.__begin_truncate_tables(name)
        self.session.commit()  # после того, как провели операции над всеми таблицами, фиксируем изменения в БД
        print(f'All tables was truncated')

    def __truncate_tables(self, table):
        """
        Приватный метод очистки таблиц
        Т.к. в sqllite отсуствует оператор truncate (очистка со сбросом значения автоинкремента), делаем руками
        :param table: имя таблицы для очистки
        """
        self.session.execute(f"DELETE FROM {table};")
        self.session.flush()
        self.session.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table}';")
        self.session.flush()
        print(f'Table {table} prepare for truncate')

    def new_post_to_bd(self, post):
        """
        Добавление новой записи в таблице Posts
        :param post: добавляемая запись
        """
        new_post = Posts(post)  # создаем экземпляр класса Posts
        #  ищем в БД пользователя по id, который указан в посте
        find_user = self.session.query(Users).filter_by(id=post['userId']).all()
        if len(find_user) == 0:  # если такого пользователя нет, то пост не добавляем (т.к. неккому привязывать)
            print('No such user!!!')
        else:
            # делаем запрос на выборку из бд строки с аналогичными параметрами поста (кроме id)
            # для исключения случаем повторного занесения информации
            find_post = self.session.query(Posts).filter_by(userId=post['userId'], title=post['title'],
                                                            body=post['body']).all()
            self.__check_result(find_post, new_post)  # отправляе результат запроса на обработку

    def new_user_to_bd(self, user):
        """
        Добавление нового пользователя в бд
        :param user: добавляемый пользователь
        """
        new_user = Users(user)
        # т.к. к таблица пользователя имеет первичные ключи на таблицы company и address, заполним сначала их
        new_user.company = self.__add_new_company(user['company'])
        new_user.address = self.__add_new_address(user['address'])
        # делаем запрос на выборку из бд строки с аналогичными параметрами пользователя (кроме id)
        # для исключения случаем повторного занесения информации
        find_user = self.session.query(Users).filter_by(name=user['name'], username=user['username'],
                                                        phone=user['phone'],
                                                        website=user['website'], address=new_user.address,
                                                        company=new_user.company, email=user['email']).all()
        self.__check_result(find_user, new_user)  # отправляе результат запроса на обработку

    def __add_new_company(self, company):
        """
        Добавление новой компании в бд
        :param company: данные добавляемой компания
        :return: id добавленной (либо существующей) записи в таблицу
        """
        new_company = Company(company)
        # делаем запрос на выборку из бд строки с аналогичными параметрами компании (кроме id)
        # для исключения случаем повторного занесения информации
        result = self.session.query(Company).filter_by(name=company['name'], catchPhrase=company['catchPhrase'],
                                                       bs=company['bs']).all()
        return self.__check_result(result, new_company)  # отправляе результат запроса на обработку

    def __add_new_address(self, address):
        """
        Добавление нового адреса в бд
        :param address: данные добавляемого адреса
        :return: id добавленной (либо существующей) записи в таблицу
        """
        new_address = Address(address)
        # т.к. к таблица пользователя имеет первичный ключ на таблицу geo(геокоординаты), заполнием сначала её
        new_address.geo = self.__add_new_geo(address['geo'])
        result = self.session. \
            query(Address). \
            filter_by(street=address['street'], suite=address['suite'], city=address['city'],
                      zipcode=address['zipcode']).all()
        return self.__check_result(result, new_address)  # отправляе результат запроса на обработку

    def __add_new_geo(self, geo):
        """
        Добавление новых координат  в БД
        :param geo - имя пользователя
        :return: id добавленной (либо существующей) записи в таблицу
        """
        geopos = Geo(geo)
        # делаем запрос на выборку из бд строки с аналогичными параметрами координат (кроме id)
        # для исключения случаем повторного занесения информации
        result = self.session.query(Geo).filter_by(lat=geopos.lat, lng=geopos.lng).all()
        return self.__check_result(result, geopos)  # отправляе результат запроса на обработку

    def __check_result(self, result, record):
        """
        Обработка результатов запроса существования записи
        :param result: рещультат запроса
        :param record: запись
        :return: id оабвленной или найденой записи
        """
        if len(result) == 0:  # если результат пуст (нет такой записи), то добавляем запись в бд и получаем ее id
            self.session.add(record)
            self.session.flush()
            row_id = record.id
            print(f'{type(record)} id #{row_id} added in bd')
        elif len(result) == 1:  # если запись существует в БД, получаем ее id
            print(f'{type(record)} id #{result[0].id} allready in bd')
            row_id = result[0].id
        else:  # если найдено более чем одна запись - генерируем исключение, т.к. данные доллжны быть уникальны
            raise
        return row_id  # возвращаем id записи
