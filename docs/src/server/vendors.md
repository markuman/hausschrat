# vendors

Vendor libraries are used as source for

* private key
* password that belongs to the private key.

Nowadays everyone uses some SaaS Cloudprovider for everything.  
For secret management, 1password or AWS SSM is widespread.  
Once one of your secret providers is breached, everything is instantly lost.  
So for security reasons, it is highly recommended not to save them at the same place, e.g. key and belonging password at 1password.  

So for example: Save the key e.g. in a S3 bucket and the password at bitwarden.

## default vendor

_hausschrats_ default vendor uses

* private key: Nextcloud
* password: lesspass

Therefor you must provide Nextcloud credentials

* `NEXTCLOUD_HOST`
* `NEXTCLOUD_USER`
* `NEXTCLOUD_TOKEN`

and the lesspass master password.

* `LESSPASS_PASSWORD`

all as env variables.

### default vendor usage

1. generate a password with `lesspass-cli`

`lesspass http://localhost:8080 hausschrat your_strong_lesspass_password -l -u -d  -s  -L 32 -C 1`

The settings are the defaults which are set in the database table `hausschrat` in `vendor_password_obj`.

```python
{
    'login': 'hausschrat',
    'site': 'http://localhost:8080',
    'lowercase': True,
    'uppercase': True,
    'symbols': True,
    'digits': True,
    'counter': 1,
    'length': 32
}
```

You can change as you like ...

2. generate a new private key


And generate a new private key. Use password from your lesspass cli above.

`ssh-keygen -t ed25519 -f hausschrat.pem`

3. save private key in your nextcloud
4. create an access key for your nextcloud for hausschrat.
5. start your docker container with the following env variables.

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

# become your own vendor.

You just need to develope a library with the class `vault` which can be importet.  
As an example, take a look add `hausschrat-nextcloud-s3` library.

It uses:

* private key: AWS S3 Bucket
* password: nextcloud password app