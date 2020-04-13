import requests
import json
import properties

from urllib.parse import urlparse, parse_qs

from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session

""" url = 'https://www.strava.com/api/v3/athlete'
data = {'before': '56','after': '56', 'page': '1', }
cert = "Bearer: %s" % (properties.token)
print (cert)

try:
    response = requests.get(url, headers = {"Authorization": cert})
    #response = requests.get(url, auth = ('Authorization', cert))
    #response = requests.get('https://api.github.com')
    #response = requests.get('https://api.github.com/invalid')

    #raise Exception if response not successful
    response.raise_for_status()

except HTTPError as http_err:
    print('HTTP error occurred: {http_err}', http_err)
except Exception as err:
    print('Other error occurred: {err}')
else:
    print('Success!') """

#response body, stored in dictionary
#payload = json.loads(response.content)

#headers, stored in dictionary
#headers = response.headers

#params = {'client_id': properties.client_id, 'response_type': 'code', 'redirect_uri': redirect_uri}

client_id = properties.client_id
client_secret = properties.client_secret
redirect_uri = 'http://localhost/exchange_token'
scope = 'read'
kwargs = {'approval_prompt': 'force'}
approval_prompt = 'force'
auth_url = 'https://www.strava.com/oauth/authorize'
token_url = 'https://www.strava.com/oauth/token'

oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=[scope])
authorization_url, state = oauth.authorization_url(auth_url)

#unable to get **kwargs to accept strava's 'approval_prompt' arg. So we literally just tack it on the end here.
#Authorization url still messes with symbols in redirect_uri but it seems to be functional
authorization_url = authorization_url + '&approval_prompt=force'

print ("Please go to " + authorization_url + " and authorize access.")
authorization_response = input('Enter the full callback URL: ')

#take response, parse out code if we got one
o = urlparse(authorization_response)
query = parse_qs(o.query)
if 'code' in query:
    authorization_code = query['code']
else:
    print ("No authorization code")

#perform token exchange using auth code
payload = {'client_id':properties.client_id, 'client_secret': properties.client_secret, 'code': authorization_code, 'grant_type': 'authorization_code'}
r = requests.post(token_url, data=payload)

if r.status_code == 200:
    print (r.json())