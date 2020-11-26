from bottle import route, request, HTTPResponse, static_file, run, hook
from uuid import uuid4
import urllib
import requests
from lib import dbv2
from lib import utils
from lib import keyHandler
from lib import scmHandler
import logging
import os
import bottle

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger('hausschrat')

@hook('before_request')
def _connect_db():
    dbv2.db.connect()

@hook('after_request')
def _close_db():
    if not dbv2.db.is_closed():
        dbv2.db.close()

@route('/')
def oh_hai():
	return HTTPResponse(status=200)

@route('/public_key')
def public_key():
    return keyHandler.public_key()

@route('/revoke')
def revoke():
    retval = utils.process_revoked_public_key(logger)
    logger.info(retval)
    if retval:
        return static_file("revoked_keys", root="/tmp")

    logger.error(" no revoked keys available")
    return HTTPResponse(status=404)
    
@route('/sign', method='POST')
def sign():

    data = request.json
    settings = dbv2.get_settings()

    if settings.get('scm_url'):
        if date.get('scm_url'):
            if settings.get('scm_url') != date.get('scm_url'):
                logger.error(" server restricted scm_url")
                return HTTPResponse(status=403)

    scm_url = settings.get('scm_url') or data.get('scm_url')
    
    if scm_url is None:
        logger.error(" scm_url not given")
        return HTTPResponse(status=401)

    ## determine scm_url backend
    ############################
    scm = scmHandler.scmHandler(scm_url, data.get('api_token'))
    scm_user = scm.get_username()
    pub_keys = scm.get_public_keys()

    logger.info(" api token is valid")

    ## find requested public key
    ############################
    pub_key, user = None, None
    for key in pub_keys:
        if data['key'] == key['title']:
            logger.info(" found requested public key")
            pub_key = key['key']
            user = scm_user
            break
    
    ## set servers default expire value
    ## when user does not request it
    ###################################
    expire = data.get('expire') or settings.get('expire')

    if None not in [pub_key, user]:
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

        ## strict_user mode.
        ## issue a certificate
        ## for user that owns
        ## the api key
        #######################
        if data.get('user') is None or data.get('user') == user:
            logger.info(" process certificate issue from {IP}".format(IP=client_ip))
            kh = keyHandler.keyHandling(pub_key, user, expire, settings)
            cert = kh.sign_key()
            return { 'cert': cert}

        ## server mode is not strict_user
        ## issue a certificate
        ## any user that is requested can
        ## issue a certificate.
        ##################################
        elif settings.get('mode') in ['open', 'host']:
            logger.info(" process certificate issue from {IP}".format(IP=client_ip))
            kh = keyHandler.keyHandling(pub_key, data.get('user'), expire, settings)
            cert = kh.sign_key()
            return { 'cert': cert}
        
        else:
            logger.error(" requested username does not match with api_token")
            return HTTPResponse(status=403)

    else:
        logger.error(" api_token is invalid for scm_url")
        return HTTPResponse(status=403)



if __name__ == '__main__':
    dbv2.init()
    run(host='0.0.0.0', port=8080)

app = bottle.default_app()