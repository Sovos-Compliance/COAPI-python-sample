from samples import helpers
import time
import config


class Authentication:
    def __init__(self):
        self._access_token = ''
        self._access_token_expire = 0
        self._api_key = config.API_KEY
        self._secret = config.SECRET_KEY
        self._base_url = config.BASE_URL
        self.last_response = {}

    def get_access_token(self):
        if (int(time.time()) >= self._access_token_expire):
            url = f"{self._base_url}/oauth/client_credential/accesstoken?grant_type=client_credentials"

            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',     
            }
            response = helpers.requests_retry_session().request(
                'POST',
                url,
                auth=(self._api_key, self._secret),
                headers=headers,
                data=payload
            )
            
            self._last_response = response.json()
            self._access_token = response.json().get('access_token')
            
            expires_in = int(response.json().get('expires_in'))
            self._access_token_expire = int(time.time()) + expires_in
            
        return self._access_token
        

    def set_access_token_expire(self, expiration_time):
        self._access_token_expire = expiration_time


auth = Authentication()