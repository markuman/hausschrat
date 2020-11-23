import tempfile
from datetime import timedelta
from datetime import datetime
import pexpect
import requests
import os
import time

from lib import db
from lib.vendors import nextcloud, aws

UNITS = {"m":"minutes", "h":"hours", "d":"days", "w":"weeks"}

def convert_to_seconds(s):
    count = int(s[:-1])
    unit = UNITS[ s[-1] ]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days


def detect_scm(scm_url):
    """
        currently hausschrat is supporting gitea and gitlab.
        gitea identification is stright forward.
        gitlab identification is tias.
    """
    t = requests.get('{url}/api/v1/version'.format(url=scm_url))
    if t.status_code == 200:
        return {
            'SCM': 'gitea',
            'check_user': '{url}/api/v1/user',
            'get_pub_keys': '{url}/api/v1/user/keys'
        }
    elif t.status_code == 503: # it's a gitlab :)
        return {
            'SCM': 'gitlab',
            'check_user': '{url}/api/v4/user',
            'get_pub_keys': '{url}/api/v4/user/keys'
        }
    
class keyHandling(object):

    def __init__(self, pub_key, user, expire, settings):
        self.priv_key_location = '/tmp/priv_key'
        self.user = user
        self.pub_key = pub_key
        self.settings = settings

        ## set vendor provider
        ######################
        if settings.get('auth_vendor') == 'nextcloud':
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
        if convert_to_seconds(default_exire) < convert_to_seconds(requested_expire):
            self.expire = default_exire
        else:
            self.expire = requested_expire
        
        ## key handling
        ## save requested public key
        ## save private key from vendor
        ###############################
        self.pub_key_file, self.pub_cert_file = self.write_pub_key(pub_key)
        self.password = self.receive_priv_key()


    def write_pub_key(self, pub_key):
        pub_key_file = "/tmp/{name}".format(name=next(tempfile._get_candidate_names())) + '.pub'
        with open(pub_key_file, 'w' ) as f:
            f.write(pub_key)

        parts = pub_key_file.split(".")
        cert_key_file = parts[0] + "-cert." + parts[1]

        return pub_key_file, cert_key_file

    def receive_priv_key(self):
        priv_key = self.vault.key()
        with open(self.priv_key_location, 'w' ) as f:
            f.write(priv_key.decode('utf-8'))
        os.chmod(self.priv_key_location, 0o600)
        return self.vault.password()

    def sign_key(self):

        authority_name = self.settings.get('authority_name')

        ## build datetime for database entry
        ####################################
        expire_datetime = str(
            datetime.fromtimestamp(
                datetime.now().timestamp() + convert_to_seconds(self.expire)
            )
        )

        ## issue a certificate
        ######################
        child = pexpect.spawn ("ssh-keygen -s {PRIV_KEY} -I {AUTHORITY} -n {USER} -V {EXPIRE} {PUBLIC_KEY}".format(
            AUTHORITY=authority_name,
            USER=self.user,
            EXPIRE=self.expire,
            PUBLIC_KEY=self.pub_key_file,
            PRIV_KEY=self.priv_key_location
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
        mariadb = db.db()
        mariadb.save_cert(self.pub_key, self.user, expire_datetime)
        mariadb.close()

        ## remove all key files
        #######################
        os.remove(self.pub_key_file)
        os.remove(self.pub_cert_file)
        os.remove(self.priv_key_location)

        return cert
        