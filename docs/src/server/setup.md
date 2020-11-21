## setup

The setup is easy, because all what _hausschrat_ needs is a valid mariadb database connection  
with a database (_utf8mb4_) names `hausschrat`.  
Once it's started, it creates two tables.

1. `hausschrat`
2. `certs`

The `hausschrat table is where the configuration lives.  
The `certs` table is where all cert public keys will be stored.
