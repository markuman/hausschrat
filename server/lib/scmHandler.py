import requests

class scmHandler(object):

    def __init__(self, scm_url, api_token):

        self.api_token = api_token
        self.scm_url = scm_url

        self.is_gitea = False
        self.is_gitlab = False

        if self.its_gitlab():
            self.is_gitlab = True
            self.headers = {
                'PRIVATE-TOKEN': self.api_token,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }

        else:
            self.is_gitea = True
            self.headers = {
                'Authorization': 'token {TOKEN}'.format(TOKEN=self.api_token),
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }

    def its_gitlab(self):

        t = requests.get('{url}/api/v1/version'.format(url=self.scm_url))
        if t.status_code == 503: # it's a gitlab :)
            return True
        elif t.status_code == 200:
            return False
        else:
            raise Exception('cannot detect scm or wrong api token')

    def get_username(self):

        if self.is_gitlab:
            requested_user = requests.get('{url}/api/v4/user'.format(url=self.scm_url),
                headers=self.headers
            )

        elif self.is_gitea:
            requested_user = requests.get('{url}/api/v1/user'.format(url=self.scm_url),
                headers=self.headers
            )
        if requested_user.status_code == 200:
            return requested_user.json().get('username')
        else:
            raise Exception('cannot fetch username')

    def get_public_keys(self):

        if self.is_gitlab:
            public_keys = requests.get('{url}/api/v4/user/keys'.format(url=self.scm_url),
                headers=self.headers
            )

        elif self.is_gitea:
            public_keys = requests.get('{url}/api/v1/user/keys'.format(url=self.scm_url),
                headers=self.headers
            )
        if public_keys.status_code == 200:
            return public_keys.json()
        else:
            raise Exception('cannot fetch public keys')