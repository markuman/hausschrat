from bottle import route, request, HTTPResponse, static_file, run
from uuid import uuid4
import urllib
import requests
from lib import db
from lib import utils

mariadb = db.db()

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

def get_default_values():
    sql = """
    select value from hausschrat where setting = 'authority_name';
    """

    sql = """
    select value from hausschrat where setting = 'expire';
    """



@route('/')
def oh_hai():
	return HTTPResponse(status=200)

@route('/sign', method='POST')
def sign():
    """
        sign request requires a body with three key/value pairs

        data:
            key: ssh key name
            api_token: Access token with read_user permissions
            scm_url: gitea or gitlab instance to use

            username: requires `strict_user: 0` server settings
            expired: user value <= server default value


        1. determin if it's a gitea or a gitlab instance
        2. validate api_token and fetch ssh public keys
            * in one step. when the api_token is invalid, server will response != 200
        3. search for ssh key name in response ssh public keys
            * when found, sign public key and return public-cert key.
    """
    data = request.json
    api = detect_scm(data['scm_url'])
    
    pub_keys = requests.get(api['get_pub_keys'].format(url=data['scm_url']),
        headers={
            'Authorization': 'token {TOKEN}'.format(TOKEN=data['api_token']),
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
    )
    if pub_keys.status_code == 200:

        pub_key, user = None, None
        for key in pub_keys.json():
            if data['key'] == key['title']:
                pub_key = key['key']
                user = key['user']['username']
                break
        
        if None not in [pub_key, user]:
            cert = utils.sign_key(pub_key, user, mariadb)
            return {'pub_key': cert}
        else:
            return HTTPResponse(status=401)

    else:
        return HTTPResponse(status=403)



if __name__ == '__main__':
    mariadb.init_db()
    run(host='0.0.0.0', port=8080)