import mariadb
import os
from pathlib import Path

class db(object):

    def __init__(self):
        self.ssl = Path("/opt/mariadb.pem")
        self.db = self.connect()

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
                database = os.environ.get('DATABASE') or 'hausschrat',)
        db.autocommit = True
        return db

    def init_db(self):
        sql = """
        create
            table if not exists
                certs(
                id bigint UNSIGNED not null AUTO_INCREMENT,
                user varchar(256) not null,
                signed datetime not null default now(),
                expired datetime not null,
                revoked bool not null default 0,
                cert varchar(256) not null,
                PRIMARY KEY(id)
            ) 
                ENGINE=InnoDB;
        """
        self.write(sql)

        sql = """
        create
            table if not exists
                hausschrat(
                setting varchar(32) not null,
                value varchar(32) not null,
                PRIMARY KEY(setting)
            ) 
            ENGINE=InnoDB;
        """
        self.write(sql)

        sql = """
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'expired',
            `value` = '1w';
        """
        self.write(sql)
        sql = """
        INSERT IGNORE INTO `hausschrat`
            SET `setting` = 'strict_user',
            `value` = 'yes';
        """
        self.write(sql)

    def write(self, sql):
        with self.db.cursor() as cursor:
            cursor.execute(sql)

    def save_cert(self, cert, user, expire):
        sql = """
        insert into certs (user, expired, cert)
            values (?, ?, ?)
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, 
                (user, expire, cert)
            )

