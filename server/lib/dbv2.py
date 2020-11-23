from datetime import datetime
import peewee
import os

if os.environ.get('MARIADB_HOST'):
    db = peewee.MySQLDatabase(
        "hausschrat",
        host=os.environ.get('MARIADB_HOST'),
        port=3306,
        user=os.environ.get('MARIADB_USER'),
        passwd=os.environ.get('MARIADB_PASSWORD')
    )

elif os.environ.get('POSTGRES_HOST'):
    db = peewee.PostgresqlDatabase(
        "hausschrat",
        host=os.environ.get('POSTGRES_HOST'),
        port=5432,
        user=os.environ.get('POSTGRES_USER'),
        passwd=os.environ.get('POSTGRES_PASSWORD')
    )

else:
    db = peewee.SqliteDatabase('/opt/hausschrat/db.sqlite')

class Hausschrat(peewee.Model):
    name = peewee.CharField(unique=True, primary_key=True)
    value = peewee.CharField()

    class Meta:
        database = db
        db_table = 'hausschrat'

class Keys(peewee.Model):
    user = peewee.CharField(unique=True)
    pub_key = peewee.CharField()
    signed = peewee.DateTimeField(default=datetime.now)
    expire = peewee.DateTimeField()
    revoked = peewee.BooleanField()

    class Meta:
        database = db
        db_table = 'keys'


def init():
    db.connect()
    Hausschrat.create_table()
    Keys.create_table()

    retval = Hausschrat.select()
    if retval.count() == 0:
        print(retval.count())

        defaults = [
            {'name': 'expire', 'value': '+1w'},
            {'name': 'mode', 'value': 'user'},
            {'name': 'authority_name', 'value': 'hausschrat'},
            {'name': 'scm_url', 'value': 'https://gitlab.com'},
            {'name': 'vendor', 'value': 'mixed'},
            {'name': 'vendor_key_location', 'value': "{'bucket': 'hausschrat', 'obj': '/hausschrat.pem'}"},
            {'name': 'vendor_password_name', 'value': 'hausschrat'},
        ]

        for item in defaults:
            try:
                hs = Hausschrat.create(name=item.get('name'), value=item.get('value'))
                hs.save()
            except:
                pass

    db.close()

def get_settings():
    db.connect()
    retval = list(Hausschrat.select().dicts())
    db.close()
    d = dict()
    for item in retval:
        d[item.get('name')] = item.get('value')
    return d


    

