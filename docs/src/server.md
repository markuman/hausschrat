# server

- [server](#server)
  * [setup](#setup)
  * [docker](#docker)
  * [backends](#backends)
  * [usage](#usage)
- [Settings](#settings)
  * [Parameter Options](#parameter-options)
    + [`expire`](#expire)
    + [`mode`](#mode)
    + [`authority_name`](#authority-name)
    + [`scm_url`](#scm-url)
    + [`vendor`](#vendor)
    + [`vendor_key_obj`](#vendor-key-obj)
    + [`vendor_password_obj_`](#vendor-password-obj)
    + [`public_key`](#public-key)
- [Revoke](#revoke)
- [Servers Public Key](#servers-public-key)


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
The db location in the container is `/opt/hausschrat/db.sqlite`. So just mount a volume to `/opt/hausschrat` to make is persistent (_or use a remote database_).

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

_hausschrat_ supports mariadb, postgres and sqlite.

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

## usage

For security reason, there is nor admin webinterface nor admin cli.  
To configure and administrate _hausschrat_ all you need is

- your favorite sql client
  * dbeaver (_highly recommended when you need a gui_)
  * mycli, sqlite3 ... etc. pp.
- sql skills (_in case that your prefered sql client does not have a gui_)

# Settings

The default values works well for most use cases.

* You may like to change the `authority_name` or the `expire` value.  
* You like to change the `scm_url`.
* You must add/provide
    * `vendor`
    * `vendor_key_obj`
    * `vendor_password_obj`

That's all.

## Parameter Options

### `expire`
Default value: `+1w` (_1 week_).

Max time until a issued certificate expired.  
The user cannot request longer durations.
Supported units are:  
`{"m":"minutes", "h":"hours", "d":"days", "w":"weeks"}`


### `mode`  
Default value: `user`  

Supported modes:

* `user`: Certificates are only issued with their `api_token` belonging user.
* `host`: Certificates are only issued to a single host. The usename doesn't matter.
* `open`: Everthing what is requested will be issued.

`host` mode is not implemented yet and is equivalent to `open` mode.

### `authority_name`
Default value: `hausschrat`

The identifier of the certificate authority.


### `scm_url`
Default value: `https://gitlab.com`  

When `scm_url` is not set, _hausschrat_ will request every source control managment tool which is requested. This is not a recommended mode and might be only useful for personal needs.    
When `scm_url` is set (_e.g. to `https://gitlab.com`), _hausschrat_ will only request it. All other requested 
source conrole managment tools are forbidden (_return status code 403_).


### `vendor`  
Default value: `default`

Defines which vendors `vault` class is used.  
When choosing another vendor, it must be importable in python and the class `vault` with the return methods `password` and `key` must exists.


### `vendor_key_obj`
Default value: `/hausschrat/hausschrat.pem`

The location of the private key for the used vendor.  
Depends on your own vauld provider, it also can be a json object.


### `vendor_password_obj`
Default value: `{"login": "hausschrat", "site": "http://localhost:8080", "lowercase": true, "uppercase": true, "symbols": true, "digits": true, "counter": 1, "length": 32}`

JSON object for the default lesspass provider.  
Depends on your own vauld provider, it also can be just a string.

### `public_key`
Default value: _not set_

This is the placeholder to the CA public key. You don't need and should not care about it.  
Once it is requested, _hausschrat_ will fetch the private key again, re-generate the public key and
save it there for performance reasons (_caching_).

# Revoke

In case you need to revoke a certificate, you must find the related row in `keys` table.  
Once it is found, just set `revoked` to `1`.  
Now you can request `https://{HAUSSCHRAT_URL}/revoke` with your orchestration and announce it to the sshd.

# Servers Public Key

You can also use the API endpoint `/public_key` in your orchestration to fetch the CA public key and announce it to the sshd.  
Once it is fetched and regenerated, it will be stored in the `hausschrat` table - for performance issue.
