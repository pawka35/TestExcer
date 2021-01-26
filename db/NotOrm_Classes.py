class Users:
    """
    Класс описывающий таблицу Users, для хранения информации по пользователям.
    """
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
        return f'Users'


class Address:
    """
    Класс описывающий таблицу Address, для хранения адресов пользователей
    """
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
        return f'Address'


class Geo:
    """
    Класс описывающий таблицу Geo для хранения информации о координатах
    """
    def __init__(self, geo):
        """
        Конструктор класса
        :param geo: объект с полями, согласно словаря geo json ответа
        """
        self.lat = geo['lat']
        self.lng = geo['lng']

    def __str__(self):
        return f'Geo'


class Company:
    """
    Класс описывающий таблицу Company для хранения информации о компании
    """
    def __init__(self, company):
        """
        Конструктор класса
        :param company: объект с полями, согласно словаря company json ответа
        """
        self.name = company['name']
        self.catchPhrase = company['catchPhrase']
        self.bs = company['bs']

    def __str__(self):
        return f'Company'


class Posts:
    """
    Класс описывающий таблицу Posts для хранения информации постов пользователей
    Имеет поле-внешний ключ от таблицы Users
    """
    def __init__(self, post):
        """
        Конструктор класса
        :param post: объект с полями json ответа
        """
        self.userId = post['userId']
        self.title = post['title']
        self.body = post['body']

    def __str__(self):
        return f'Posts'
