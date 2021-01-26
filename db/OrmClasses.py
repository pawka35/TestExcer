from sqlalchemy import Column, Integer,  String, FLOAT, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    """
    Класс описывающий таблицу Users, для хранения информации по пользователям.
    Имеет поля, представляющие внешние ключи от таблиц Company и Address
    """
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    company = Column(Integer, ForeignKey('Company.id'))
    address = Column(Integer, ForeignKey('Address.id'))

    def __init__(self, user):
        """
        Конструктор класса
        :param user: объект с полями, согласно json ответа
        """
        self.name = user['name']
        self.username = user['username']
        self.email = user['email']
        self.phone = user['phone']
        self.website = user['website']

    def __str__(self):
        return f'{self.name}'


class Address(Base):
    """
    Класс описывающий таблицу Address, для хранения адресов пользователей
    """
    __tablename__ = 'Address'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    suite = Column(String)
    city = Column(String)
    zipcode = Column(Integer)
    geo = Column(Integer, ForeignKey('Geo.id'))

    def __init__(self, address):
        """
        Конструктор класса
        :param address: объект с полями, согласно словаря address json ответа
        """
        self.street = address['street']
        self.suite = address['suite']
        self.city = address['city']
        self.zipcode = address['zipcode']

    def __str__(self):
        return f'{self.zipcode},{self.city},{self.street},{self.suite} ({self.geo})'


class Geo(Base):
    """
    Класс описывающий таблицу Geo для хранения информации о координатах
    """
    __tablename__ = 'Geo'
    id = Column(Integer, primary_key=True)
    lat = Column(FLOAT)
    lng = Column(FLOAT)

    def __init__(self, geo):
        """
        Конструктор класса
        :param geo: объект с полями, согласно словаря geo json ответа
        """
        self.lat = geo['lat']
        self.lng = geo['lng']

    def __str__(self):
        return f'lat: {self.lat}, long: {self.lng}'


class Company(Base):
    """
    Класс описывающий таблицу Company для хранения информации о компании
    """
    __tablename__ = 'Company'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    catchPhrase = Column(String)
    bs = Column(String)

    def __init__(self, company):
        """
        Конструктор класса
        :param company: объект с полями, согласно словаря company json ответа
        """
        self.name = company['name']
        self.catchPhrase = company['catchPhrase']
        self.bs = company['bs']

    def __str__(self):
        return f'{self.name},{self.catchphrase},{self.bs}'


class Posts(Base):
    """
    Класс описывающий таблицу Posts для хранения информации постов пользователей
    Имеет поле-внешний ключ от таблицы Users
    """
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Users.id'))
    title = Column(String)
    body = Column(Text)

    def __init__(self, post):
        """
        Конструктор класса
        :param post: объект с полями json ответа
        """
        self.userId = post['userId']
        self.title = post['title']
        self.body = post['body']

    def __str__(self):
        return f'{self.userid}, {self.title}'
