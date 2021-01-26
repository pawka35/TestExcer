from django.db import models


class Address(models.Model):
    street = models.CharField(blank=True, null=True, max_length=250)
    suite = models.CharField(blank=True, null=True, max_length=250)
    zipcode = models.TextField(blank=True, null=True)  # This field type is a guess.
    geo = models.ForeignKey('Geo', models.DO_NOTHING, db_column='geo', blank=True, null=True)
    city = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return f'{self.zipcode},{self.city},{self.street},{self.suite} ({self.geo})'

    class Meta:
        managed = False
        db_table = 'Address'
        verbose_name = 'Адреса'
        verbose_name_plural = 'Адрес'


class Company(models.Model):
    name = models.TextField()  # This field type is a guess.
    catchphrase = models.TextField(db_column='catchPhrase', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    bs = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return f'{self.name},{self.catchphrase},{self.bs}'

    class Meta:
        managed = False
        db_table = 'Company'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компания'


class Geo(models.Model):
    lat = models.TextField(blank=True, null=True)  # This field type is a guess.
    lng = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Geo'
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return f'lat: {self.lat}, long: {self.lng}'


class Posts(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)  # This field type is a guess.
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Posts'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.userid}, {self.title}'


class Users(models.Model):
    name = models.TextField()  # This field type is a guess.
    username = models.TextField()  # This field type is a guess.
    phone = models.TextField(blank=True, null=True)  # This field type is a guess.
    website = models.TextField(blank=True, null=True)  # This field type is a guess.
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='address', blank=True, null=True)
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='company', blank=True, null=True)
    email = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name}'