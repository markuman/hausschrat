#!/bin/sh

# initialize the database
python3 lib/dbv2.py

if [[ -z "${SSL}" ]]; then
    # SSL was not requested
    gunicorn -w 5 --bind 0.0.0.0:8080 main:app
else
    if [ ! -f /opt/hausschrat/sslkey.pem ]; then
        # SSL was requested, but not server.key was provided
        # create self-signed
        openssl req -x509 -newkey rsa:4096 -keyout /opt/hausschrat/sslkey.pem \
            -out /opt/hausschrat/sslcert.pem -days 365 -nodes -subj "/C=EU/ST=EU/L=EU/O=lynis/CN=lynis-bridge"
    fi
    # SSL was requested with a server.key
    gunicorn -w 5 --ssl-version TLSv1_2 --certfile=/opt/hausschrat/sslcert.pem --keyfile=/opt/hausschrat/sslkey.pem --bind 0.0.0.0:8080 main:app
fi






