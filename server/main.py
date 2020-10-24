from bottle import route, request, HTTPResponse, static_file, run
from uuid import uuid4
import urllib
import requests


def detect_scm(scm_url):
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

def sign_key():
    return True

@route('/')
def oh_hai():
	return HTTPResponse(status=200)

@route('/sign', method='POST')
def sign():
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
            return {'pub_key': pub_key, 'user': user}
        else:
            return HTTPResponse(status=401)

    else:
        return HTTPResponse(status=403)



if __name__ == '__main__':
	run(host='0.0.0.0', port=8080)