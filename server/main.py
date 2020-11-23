from bottle import route, request, HTTPResponse, static_file, run
from uuid import uuid4
import urllib
import requests
from lib import db
from lib import utils
import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger('hausschrat')

@route('/')
def oh_hai():
	return HTTPResponse(status=200)

@route('/sign', method='POST')
def sign():
    """
        data requested by user

        data:
            key: ssh key name
            api_token: Access token with read_user permissions

            scm_url: optional
            username: requires `mode: open or host` server settings
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
    
    if scm_url is None:
        logger.error(" scm_url not given")
        return HTTPResponse(status=401)

    ## determine scm_url backend
    ############################
    api = utils.detect_scm(scm_url)

    ## fetch user's public keys
    ############################
    pub_keys = requests.get(api['get_pub_keys'].format(url=scm_url),
        headers={
            'Authorization': 'token {TOKEN}'.format(TOKEN=data.get('api_token')),
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }
    )

    if pub_keys.status_code == 200:
        logger.info(" api token is valid")

        ## find requested public key
        ############################
        pub_key, user = None, None
        for key in pub_keys.json():
            if data['key'] == key['title']:
                logger.info(" found requested public key")
                pub_key = key['key']
                user = key['user']['username']
                break
        
        ## set servers default expire value
        ## when user does not request it
        ###################################
        expire = data.get('expire') or settings.get('expire')

        if None not in [pub_key, user]:
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

            ## strict_user mode.
            ## issue a certificate
            #######################
            if data.get('username') is None or data.get('username') == user:
                logger.info(" process certificate issue from {IP}".format(IP=client_ip))
                kh = utils.keyHandling(pub_key, user, expire, settings)
                cert = kh.sign_key()
                return { 'cert': cert}

            ## server mode is not strict_user
            ## issue a certificate
            ##################################
            elif mariadb.get_value('mode') in ['open', 'host']:
                logger.info(" process certificate issue from {IP}".format(IP=client_ip))
                kh = utils.keyHandling(pub_key, data.get('username'), expire, settings)
                cert = kh.sign_key()
                return { 'cert': cert}
            
            else:
                logger.error(" requested username does not match with api_token")
                return HTTPResponse(status=403)
        else:
            logger.error(" user or public key not found")
            return HTTPResponse(status=401)

    else:
        logger.error(" api_token is invalid for scm_url")
        return HTTPResponse(status=403)



if __name__ == '__main__':
    mariadb = db.db()
    mariadb.init_db()
    mariadb.close()
    run(host='0.0.0.0', port=8080)