
print(dateparser.parse("now"))
print(dateparser.parse("now-30s"))

import dateparser
import tempfile

from datetime import timedelta

UNITS = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days", "w":"weeks"}
def convert_to_seconds(s):
    count = int(s[:-1])
    unit = UNITS[ s[-1] ]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days

def write_pub_key(pub_key):
    pub_key_file = "/tmp/{name}".format(name=next(tempfile._get_candidate_names())) + '.pub'
    with open(pub_key_file, 'w' ) as f:
        f.write(pub_key)

    parts = pub_key_file.split(".")
    cert_key_file = parts[0] + "-cert." + parts[1]

    return pub_key_file, cert_key_file


def sign_key(pub_key, user, mariadb):

    expire, authority_name, strict_user = mariadb.get_default_values()
    pub_key_file, cert_key_file = write_pub_key(pub_key)

    stream = os.popen("ssh-keygen -s /opt/hausschrat.key -I {AUTHORITY} -n {USER} -V {EXPIRE} {PUBLIC_KEY}".format(
        AUTHORITY=authority_name,
        USER=user,
        EXPIRE=expire,
        PUBLIC_KEY=pub_key_file
    ))
    raw = stream.read()
    expired_date = dateparser.parse("now+{EXP}".format(EXP=expire))

    with open(cert_key_file, 'r') as f
        cert = f.read()
    os.remove(pub_key_file)
    os.remove(cert_key_file)

    mariadb.save_cert(user, expired_date, cert)
    return cert