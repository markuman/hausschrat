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

        defaults = [
            {'name': 'expire', 'value': '+1w'},
            {'name': 'mode', 'value': 'user'},
            {'name': 'authority_name', 'value': 'hausschrat'},
            {'name': 'scm_url', 'value': 'https://gitlab.com'},
            {'name': 'vendor', 'value': 'mixed'},
            {'name': 'vendor_key_location', 'value': '{"bucket": "hausschrat", "obj": "/hausschrat.pem"}'},
            {'name': 'vendor_password_name', 'value': 'hausschrat'},
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

    # works fine
    data = list(Keys().select().dicts())
    print(data)

    data = Keys.create(
        name='m',
        pub_key='sowas',
        signed=datetime.now(),
        expire=datetime.now(),
    )
    data.save()

    data = Keys.create(
        name='m',
        pub_key='nicht',
        signed=datetime.now(),
        expire=datetime.now(),
        revoked=True
    )
    data.save()


    # dafuq?
    data = list(Keys().select(Keys.pub_key).where(Keys.revoked == True).dicts())
    print(data)

