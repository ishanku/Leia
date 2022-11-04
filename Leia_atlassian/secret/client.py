from Leia_atlassian.models.connect import SecurityContext
from Roja.Totes.core.utils.logger import *
import jwt

def get_client_key(url):
    host = url.split("atlassian.net")[0] + "atlassian.net"
    sc = SecurityContext.objects.get(host=host)
    return sc.client_key

def get_shared_secret(client_key):
    sc = SecurityContext.objects.get(client_key=client_key)
    return sc.shared_secret

class security:
    def create_token(self, method, url):
        token = SecurityContext.create_token(self, method, url)
        print(":::::::::::2::::::token using security context::::: " + token)
        return token

class decoder:
    algorithms = ('HS256',)
    leeway = 90
    opts = {"start_at": 0}

    def decode_claims(self, token, algorithms = algorithms):
        claims = jwt.decode(token, algorithms=algorithms,
                            options={"verify_signature": False})
        return claims