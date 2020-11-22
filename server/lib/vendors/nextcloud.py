import requests
import os

"""
VAULT VENDOR PROTOTYPE

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
        self.path = key_location
        self.password_name = password_name


    def key(self):
        r = requests.get(
            'https://{HOST}/remote.php/dav/files/{USER}/{PATH}'.format(
                HOST=self.HOST, 
                USER=self.USER,
                PATH=self.path),
            auth=(self.USER, self.TOKEN)
        )

        if r.status_code == 200:
            return r.content
        elif r.status_code == 404:
            raise Exception('key {key} does not exists'.format(key=self.path))
        else:
            raise Exception('FATAL: Unknown error')

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
