import tempfile
from datetime import timedelta
from datetime import datetime
import requests
import os
import time
from lib import dbv2

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

def process_revoked_public_key(logger):
    keys = dbv2.Keys
    revoked_pub_keys = list(keys.select(keys.pub_key).where(keys.revoked == True).dicts())

    revoke_file = "/tmp/revoked_keys"
    logger.info( "found {COUNT} revoked keys".format(COUNT=len(revoked_pub_keys)))
    remove_list = list()

    if len(revoked_pub_keys) > 0:

        if os.path.exists(revoke_file):
            os.remove(revoke_file)
        
        pub_key_file, doesnmatter = write_pub_key(revoked_pub_keys[0].get('pub_key'))
        
        os.popen("ssh-keygen -kf {RF} -z 1 {PKF}".format(
            RF=revoke_file,
            PKF=pub_key_file
        ))

        remove_list.append(pub_key_file)

    else:
        return None

    if len(revoked_pub_keys) > 1:
        n = 1
        while n < len(revoked_pub_keys):
            pub_key_file, doesnmatter = write_pub_key(revoked_pub_keys[n].get('pub_key'))

            n += 1
            os.popen("ssh-keygen -ukf {RF} -z {n} {PKF}".format(
                RF=revoke_file,
                PKF=pub_key_file,
                n=n
            ))

            remove_list.append(pub_key_file)

    time.sleep(1) # lol it's to fast and ssh-keygen stale something ...
    for item in remove_list:
        logger.info("delete {file}".format(file=item))
        os.remove(item)

    return revoke_file

def tmpname():
    return "/tmp/{name}".format(name=next(tempfile._get_candidate_names()))

def write_pub_key(pub_key):
    pub_key_file = tmpname() + '.pub'
    with open(pub_key_file, 'w' ) as f:
        f.write(pub_key)

    parts = pub_key_file.split(".")
    cert_key_file = parts[0] + "-cert." + parts[1]

    return pub_key_file, cert_key_file
