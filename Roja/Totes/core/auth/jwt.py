from atlassian_jwt import encode_token
from Leia_atlassian.models.connect import *

start_at = 0
max_results = 1000
jql = None

def Jwt():
    uri_search_pattern = f'/rest/api/3/search?${jql}s&startAt=${start_at}s&maxResults=${max_results}s'
    key = 'b1c7cfe8-9f87-3f19-83f2-83e38a5ae089'
    shared_secret = 'ATCObQrv98enQA7YN6wo6GrDqqQCiDO4rQDdZCdAfHVJURZW9Peil5UKlg'
    token = encode_token("POST", uri_search_pattern, key, shared_secret)
    print("Token  --- " + token)
    return token, key, shared_secret

