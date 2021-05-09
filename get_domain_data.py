import requests
import json

client_id = 'client_803f49b3d62e60f5b477b2561cc3f606'
client_secret = 'secret_5064d4ca320f0c7225df79355b2ee47e'
scopes = ['api_properties_read']
auth_url = 'https://auth.domain.com.au/v1/connect/token'
url_endpoint = 'https://api.domain.com.au/v1/properties/'
property_id = 'RF-8884-AK'


def get_property_info():
    response = requests.post(auth_url, data = {
                        'client_id':client_id,
                        'client_secret':client_secret,
                        'grant_type':'client_credentials',
                        'scope':scopes,
                        'Content-Type':'text/json'
                        })
    json_res = response.json()
    access_token=json_res['access_token']
    print(access_token)
    auth = {'Authorization':'Bearer ' + access_token}
    url = url_endpoint + property_id
    res1 = requests.get(url, headers=auth)    
    r = res1.json()
    print(r)


get_property_info()