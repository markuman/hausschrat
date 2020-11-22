import tempfile
from datetime import timedelta

from lib.vendors import nextcloud, aws

UNITS = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days", "w":"weeks"}
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

    def __init__(self, pub_key, user, mariadb):
        self.priv_key_location = '/tmp/priv_key'
        self.user = user
        self.mariadb = mariadb
        vendor = mariadb.get_value('auth_vendor')
        if vendor == 'nextcloud':
            self.vault = nextcloud.vault()
        elif vendor == 'aws':
            self.vault = aws.vault()

        self.pub_key_file, self.pub_cert_file = self.write_pub_key(pub_key)
        self.password = receive_priv_key()


    def write_pub_key(pub_key):
        pub_key_file = "/tmp/{name}".format(name=next(tempfile._get_candidate_names())) + '.pub'
        with open(pub_key_file, 'w' ) as f:
            f.write(pub_key)

        parts = pub_key_file.split(".")
        cert_key_file = parts[0] + "-cert." + parts[1]

        return pub_key_file, cert_key_file

    def receive_priv_key(self):
        priv_key = self.vault.key()
        with open(pub_key_file, 'w' ) as f:
            f.write(self.priv_key_location)
        return self.vault.password()

    def sign_key(self):

        expire = self.mariadb.get_value('expired')
        authority_name = self.mariadb.get_value('authority_name')

        stream = os.popen("ssh-keygen -s {PRIV_KEY} -I {AUTHORITY} -n {USER} -V {EXPIRE} {PUBLIC_KEY}".format(
            AUTHORITY=authority_name,
            USER=self.user,
            EXPIRE=expire,
            PUBLIC_KEY=self.pub_key_file,
            PRIV_KEY=self.priv_key_location
        ))
        raw = stream.read()
        #expired_date = dateparser.parse("now+{EXP}".format(EXP=expire))

        with open(self.cert_key_file, 'r') as f:
            self.mariadb.save_cert(user, expired_date, f.read())
        os.remove(self.pub_key_file)
        os.remove(self.cert_key_file)
        os.remove(self.priv_key_location)

        
        return cert

