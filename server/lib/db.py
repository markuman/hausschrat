import mariadb
import os
from pathlib import Path

class db(object):

    def __init__(self):
        self.ssl = Path("/opt/mariadb.pem")
        self.db = self.connect()

    def close(self):
        self.db.close()

    def connect(self):
        if self.ssl.is_file():
            db = mariadb.connect(
                host = os.environ.get('DATABASE_HOST') or 'mariadb',
                port = 3306,
                user = os.environ.get('DATABASE_USER') or 'hausschrat',
                password = os.environ.get('DATABASE_PASSWORD') or 'hausschrat',
                database = os.environ.get('DATABASE') or 'hausschrat',
                ssl_ca = '/opt/mariadb.pem')
        else:
            db = mariadb.connect(
                host = os.environ.get('DATABASE_HOST') or 'mariadb',
                port = 3306,
                user = os.environ.get('DATABASE_USER') or 'hausschrat',
                password = os.environ.get('DATABASE_PASSWORD') or 'hausschrat',
                database = os.environ.get('DATABASE') or 'hausschrat')
        db.autocommit = True
        return db

    def init_db(self):
        QUERIES = ["""
        create
            table if not exists
                certs(
                id bigint UNSIGNED not null AUTO_INCREMENT,
                user varchar(256) not null,
                signed datetime not null default now(),
                expired datetime not null,
                revoked bool not null default 0,
                pub_key varchar(256) not null,
                PRIMARY KEY(id)
            ) 
                ENGINE=InnoDB;
        """,
        """
        create
            table if not exists
                hausschrat(
                setting varchar(32) not null,
                value varchar(32) not null,
                PRIMARY KEY(setting)
            ) 
            ENGINE=InnoDB;
        """,
        """
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'expire',
            `value` = '1w';
        """,
        """
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'mode',
            `value` = 'user';
        """,
        """
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'authority_name',
            `value` = 'hausschrat';
        ""","""
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'scm_url',
            `value` = 'https://gitlab.com';
        ""","""
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'auth_vendor',
            `value` = 'nextcloud';
        """]

        for sql in QUERIES:
            self.write(sql)

    def write(self, sql):
        with self.db.cursor() as cursor:
            cursor.execute(sql)

    def save_cert(self, cert, user, expire):
        sql = """
        insert into certs (user, expired, pub_key)
            values (?, ?, ?);
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, 
                (user, expire, cert)
            )

    def get_value(self, setting):
        sql = """
        select value from hausschrat where setting = '{SETTING}';
        """.format(SETTING=setting)
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            retval = cursor.fetchall()
        try:
            return retval[0][0]
        except:
            return None

    def get_settings(self):
        sql = "select setting, value from hausschrat;"
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            retval = cursor.fetchall()
        return dict(retval)

    def revoked_certs(self):
        sql = """
        select cert from certs where expired > now() and revoked = 1;
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            retval = cursor.fetchall()
        
        return retval