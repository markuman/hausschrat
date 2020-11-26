from datetime import datetime
import peewee
import os
import json

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
    value = peewee.CharField(max_length=600)

    class Meta:
        database = db
        db_table = 'hausschrat'

class Keys(peewee.Model):
    user = peewee.CharField()
    pub_key = peewee.CharField(max_length=600)
    signed = peewee.DateTimeField(default=datetime.now)
    expire = peewee.DateTimeField()
    revoked = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'keys'


def init():
    db.connect() # valid because it's init()
    Hausschrat.create_table()
    Keys.create_table()

    retval = Hausschrat.select()
    if retval.count() == 0:

        lesspass_default_profile = {'login': 'hausschrat',
                                'site': 'http://localhost:8080',
                                'lowercase': True,
                                'uppercase': True,
                                'symbols': True,
                                'digits': True,
                                'counter': 1,
                                'length': 32}

        defaults = [
            {'name': 'expire', 'value': '+1w'},
            {'name': 'mode', 'value': 'user'},
            {'name': 'authority_name', 'value': 'hausschrat'},
            {'name': 'scm_url', 'value': 'https://gitlab.com'},
            {'name': 'vendor', 'value': 'default'},
            {'name': 'vendor_key_obj', 'value': '/hausschrat/hausschrat.pem'},
            {'name': 'vendor_password_obj', 'value': json.dumps(lesspass_default_profile)},
        ]

        for item in defaults:
            try:
                hs = Hausschrat.create(name=item.get('name'), value=item.get('value'))
                hs.save()
            except:
                pass

    db.close() # valid because it's init()

def get_settings():
    retval = list(Hausschrat.select().dicts())
    d = dict()
    for item in retval:
        d[item.get('name')] = item.get('value')
    return d


if __name__ == '__main__':
    init()
