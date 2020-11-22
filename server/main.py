from bottle import route, request, HTTPResponse, static_file, run
from uuid import uuid4
import urllib
import requests
from lib import db
from lib import utils


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

            username: requires `strict_user: 0` server settings
            expire: user value <= server default value


        1. determin if it's a gitea or a gitlab instance
        2. validate api_token and fetch ssh public keys
            * in one step. when the api_token is invalid, server will response != 200
        3. search for ssh key name in response ssh public keys
            * when found, sign public key and return public-cert key.
    """
    data = request.json
    mariadb = db.db()
    settings = mariadb.get_settings()
    mariadb.close()
    scm_url = settings.get('scm_url') or data.get('scm_url')
    api = utils.detect_scm(scm_url)
    
    pub_keys = requests.get(api['get_pub_keys'].format(url=scm_url),
        headers={
            'Authorization': 'token {TOKEN}'.format(TOKEN=data.get('api_token')),
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
        expire = data.get('expire') or settings.get('expire')
        if None not in [pub_key, user]:

            if data.get('username') is None or data.get('username') == user:
                kh = utils.keyHandling(pub_key, user, expire, settings)
                cert = kh.sign_key()
                return { 'cert': cert}

            elif mariadb.get_value('mode') in ['open', 'host']:
                kh = utils.keyHandling(pub_key, data.get('username'), expire, settings)
                cert = kh.sign_key()
                return { 'cert': cert}
            
                
            else:
                return HTTPResponse(status=403)
        else:
            return HTTPResponse(status=401)

    else:
        return HTTPResponse(status=403)



if __name__ == '__main__':
    mariadb = db.db()
    mariadb.init_db()
    mariadb.close()
    run(host='0.0.0.0', port=8080)