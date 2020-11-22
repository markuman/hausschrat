## setup

The setup is easy, because all what _hausschrat_ needs is a valid mariadb database connection  
with a database (_utf8mb4_) names `hausschrat`.  
Once it's started, it creates two tables.

1. `hausschrat`
2. `certs`

The `hausschrat table is where the configuration lives.  
The `certs` table is where all public keys will be stored where _hausschrat_ has issued a certificate.  
This is essential to generate revoke files.

When it is deployed, you only need to make very few settings changes for your needs in the `hausschrat` table.

## docker

Basically that's all.

```
docker run -ti --rm --name hausschrat \
    -e DATABASE_HOST=some_host \
    -e DATABASE_USER=hausschrat \
    -e DATABASE_PASSWORD=some_password \
    -p 8000:8000 \
    hausschrat:1
```

But you need to provide credentials for your vault provider(s).  
In case of Nextcloud, it looks like that:


```
docker run -ti --rm --name hausschrat \
    -e DATABASE_HOST=some_host \
    -e DATABASE_USER=hausschrat \
    -e DATABASE_PASSWORD=some_password \
    -e NEXTCLOUD_HOST=nextcloud.domain.tld \
    -e NEXTCLOUD_USER=username \
    -e NEXTCLOUD_TOKEN=abc \
    -p 8000:8000 \
    hausschrat:1
```