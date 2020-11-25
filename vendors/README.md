## hausschrat-nextcloud-s3 vendor

_hausschrats_ nextcloud s3 vendor

* private key: s3 bucket
* password: nextcloud passwords app

## install

`pip3 install hausschrat_nextcloud_s3`

## credentials

Therefor you must provide Nextcloud credentials

* `NEXTCLOUD_HOST`
* `NEXTCLOUD_USER`
* `NEXTCLOUD_TOKEN`

Credentials for S3 (_boto3_) are taken from ECSTaskRole, InstanceRole or from your default aws config.

## settings

In `hausschrat` table set 

* `vendor` to `hausschrat_nextcloud_s3`
* `vendor_key_obj` to `{'bucket': 'your-bucket', 'obj': 'path/so/hausschrat.pem'}`.
* `vendor_password_obj` to `hausschrat` (_name of your password in passwords app_).