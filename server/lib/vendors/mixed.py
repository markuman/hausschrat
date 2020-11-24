import os
import requests
import boto3
import json
from io import BytesIO

"""
VAULT VENDOR PROTOTYPE

Private Key is fetched from aws s3 bucket.
Belonging password is fetched from Nextcloud.

class: vault
    init arguments:
        - key_location
          location where to find the private key
        - password_name
          location where to find the password for the private key

        ENV Variables
            - NEXTCLOUD_HOST
            - NEXTCLOUD_TOKEN
            - NEXTCLOUD_USER

    methods:
        - key
          return private key as string
        - password
          return password as string
"""
class vault(object):

    def __init__(self, key_location, password_name):
        self.HOST = os.environ.get('NEXTCLOUD_HOST')
        self.TOKEN = os.environ.get('NEXTCLOUD_TOKEN')
        self.USER = os.environ.get('NEXTCLOUD_USER')
        self.password_name = password_name
        self.client = boto3.client('s3')
        print(key_location)
        j = json.loads(key_location)
        self.bucket = j.get('bucket')
        self.obj = j.get('obj')

    def key(self):
        f = BytesIO()
        try:
            self.client.download_fileobj(self.bucket, self.obj, f)
            retval = f.getvalue()

            return retval
        except:
            raise Exception('key not found or missing access permissions')


    def password(self):
        r = requests.get(
            'https://{HOST}/index.php/apps/passwords/api/1.0/password/list'.format(
                HOST=self.HOST
            ),
            auth=(self.USER, self.TOKEN)
        )

        if r.status_code == 200:
            for item in r.json():
                if item['label'] == self.password_name:
                    return item['password']

            return None
        else:
            raise Exception('Cannot access nextcloud passwords')

        return r
