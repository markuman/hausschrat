import os
import json
import requests
from lesspass.password import generate_password

"""
VAULT VENDOR DEFAULT

class: vault
    init arguments:
        - key
          location where to find the private key
        - password
          lesspass profile to calculate privatekey password

        ENV Variables
            - NEXTCLOUD_HOST
            - NEXTCLOUD_TOKEN
            - NEXTCLOUD_USER
            - LESSPASS_PASSWORD

    methods:
        - key
          return private key as string
        - password
          return password as string
"""
class vault(object):

    def __init__(self, key, password):
        self.HOST = os.environ.get('NEXTCLOUD_HOST')
        self.TOKEN = os.environ.get('NEXTCLOUD_TOKEN')
        self.USER = os.environ.get('NEXTCLOUD_USER')
        self.path = key
        self.profile = json.loads(password)
        self.secret = os.environ.get('LESSPASS_PASSWORD')

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

        return generate_password(self.profile, self.secret)
