## setup

The setup is easy, because all what _hausschrat_ needs is a valid database connection  
with a database named `hausschrat` (_in case of mariadb or postgres_).  
Once it's started, it creates two tables.

1. `hausschrat`
2. `keys`

The `hausschrat` table is where the configuration lives.  
The `keys` table is where all public keys will be stored where _hausschrat_ has issued a certificate.  
This is essential to generate revoke files.

When it is deployed, you only need to make very few settings changes for your needs in the `hausschrat` table. See "usage" for more.

## docker

You can start with `sqlite3`.  
`/mnt/hausschrat/` volume is used that for the sqlite3 database.
```
docker run -ti --rm --name hausschrat \
    -v /mnt/hausschrat/:/opt/hausschrat \
    -p 8080:8080 \
    hausschrat:1
```

But you need to provide credentials for your vault provider(s).  
In case of `default` vendor, you need

* `NEXTCLOUD_HOST`
* `NEXTCLOUD_USER`
* `NEXTCLOUD_TOKEN`
* `LESSPASS_PASSWORD`

```
docker run -ti --rm --name hausschrat \
    -v /mnt/hausschrat/:/opt/hausschrat \
    -e NEXTCLOUD_HOST=nextcloud.domain.tld \
    -e NEXTCLOUD_USER=username \
    -e NEXTCLOUD_TOKEN=abc \
    -e LESSPASS_PASSWORD=your_strong_lesspass_password \
    -p 8080:8080 \
    hausschrat:1
```

## backends

_hausschrat_ supports mariadb, postgres or sqlite.

When `MARIADB_HOST` is given, it uses mariadb/mysql.  
When `POSTGRES_HOST` is given, it uses postgres.  
When none is given, it uses sqlite in location `/opt/hausschrat/db.sqlite`

| variables | mariadb | postgres |
| --- | --- | --- |
| Database Host | `MARIADB_HOST` | `POSTGRES_HOST` |
| Database User | `MARIADB_USER` | `POSTGRES_USER` |
| Database Password | `MARIADB_PASSWORD` | `POSTGRES_PASSWORD` |
| Port | set to default `3306` | set to default `5432` |
| Database | hardcoded to `hausschrat` | hardcoded to `hausschrat` | 
