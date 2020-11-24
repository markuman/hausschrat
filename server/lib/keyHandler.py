import tempfile
from datetime import timedelta
from datetime import datetime
import pexpect
import requests
import os
import time

from lib import dbv2
from lib import utils
from lib.vendors import nextcloud, aws

priv_key_location = '/tmp/priv_key'

def receive_priv_key(vault):
    priv_key = vault.key()
    with open(priv_key_location, 'w' ) as f:
        f.write(priv_key.decode('utf-8'))
    os.chmod(priv_key_location, 0o600)
    return vault.password()

def public_key():
    settings = dbv2.get_settings()

    if pk := settings.get('public_key'):
        return pk

    ## set vendor provider
    ######################
    if settings.get('vendor') == 'nextcloud':
        vault = nextcloud.vault(
            settings.get('vendor_key_location'),
            settings.get('vendor_password_name')
        )
    elif settings.get('auth_vendor') == 'aws':
        vault = aws.vault()

    password = receive_priv_key(vault)

    child = pexpect.spawn ('ssh-keygen -y -f {KEY}'.format(KEY=priv_key_location))
    child.expect('Enter passphrase: ')
    child.sendline (password)
    retval = child.read().decode('utf-8').strip()
    os.remove(priv_key_location)
    Hausschrat = dbv2.Hausschrat
    data = Hausschrat.create(name='public_key', value=retval)
    data.save()
    return retval

class keyHandling(object):

    def __init__(self, pub_key, user, expire, settings):
        self.priv_key_location = '/tmp/priv_key'
        self.user = user
        self.pub_key = pub_key
        self.settings = settings

        ## set vendor provider
        ######################
        if settings.get('vendor') == 'nextcloud':
            self.vault = nextcloud.vault(
                settings.get('vendor_key_location'),
                settings.get('vendor_password_name')
            )
        elif settings.get('auth_vendor') == 'aws':
            self.vault = aws.vault()

        ## cap expire value
        ## in case user requests to large value
        #######################################
        default_exire = settings.get('expire')
        requested_expire = expire
        if utils.convert_to_seconds(default_exire) < utils.convert_to_seconds(requested_expire):
            self.expire = default_exire
        else:
            self.expire = requested_expire
        
        ## key handling
        ## save requested public key
        ## save private key from vendor
        ###############################
        self.pub_key_file, self.pub_cert_file = utils.write_pub_key(pub_key)
        self.password = receive_priv_key(self.vault)

    def sign_key(self):

        authority_name = self.settings.get('authority_name')

        ## build datetime for database entry
        ####################################
        expire_datetime = str(
            datetime.fromtimestamp(
                datetime.now().timestamp() + utils.convert_to_seconds(self.expire)
            )
        )

        ## issue a certificate
        ######################
        child = pexpect.spawn("ssh-keygen -s {PRIV_KEY} -I {AUTHORITY} -n {USER} -V {EXPIRE} {PUBLIC_KEY}".format(
            AUTHORITY=authority_name,
            USER=self.user,
            EXPIRE=self.expire,
            PUBLIC_KEY=self.pub_key_file,
            PRIV_KEY=priv_key_location
        ))
        child.expect ('Enter passphrase: ')
        child.sendline (self.password)

        if child.exitstatus is None:
            time.sleep(2)

        ## read issued certificate
        ##########################
        with open(self.pub_cert_file, 'r') as f:
            cert = f.read()
        
        ## save requested public key in db
        ## might be requested for revoke later
        ######################################
        Keys = dbv2.Keys()
        data = Keys.create(
            user=self.user,
            pub_key=self.pub_key,
            expire=expire_datetime,
        )
        data.save()

        ## remove all key files
        #######################
        os.remove(self.pub_key_file)
        os.remove(self.pub_cert_file)
        os.remove(priv_key_location)

        return cert
        