import boto3
import os

"""
VAULT VENDOR AWS

class: vault
    init arguments:
        - key_location
          location where to find the private key
        - password_name
          location where to find the password for the private key

        ENV Variable
          - region (optional)

        Access Key and Secret are autodetect by boto3 (prefered to use instance/ecs task role)

    methods:
        - key
          return private key as string
        - password
          return password as string


"""
class vault(object):

    def __init__(self, key_location, password_name):
        pass


    def key(self):
        pass

    def password(self):
        pass