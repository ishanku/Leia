"""Authenticate an HTTP request that contains an Atlassian-style JWT token.

Atlassian-style JWT tokens include a `qsh` claim which stands for query string
hash. See `Understanding JWT for Atlassian Connect`_ for more details.

.. Understanding JWT for Atlassian Connect
   _https://developer.atlassian.com/blog/2015/01/understanding-jwt/
"""
from Roja.Totes.core.utils.logger import *
import abc
import collections
from Roja.Totes.auth.connect import *
import jwt as jwt
from jwt import DecodeError

from .url_utils import hash_url, parse_query_params


def getAuthenticated(url, params, headers, algorithms, leeway=90, jwt_token=None, token=None):
    # token = Authenticator._get_token(
    #     headers=headers,
    #     query_params=parse_query_params(url))
    http_method = 'GET'
    if not jwt_token:
        print("get token")
        token = Authenticator._get_token(
            headers=headers,
            query_params=parse_query_params(url))

    claims = jwt.decode(jwt_token, algorithms=algorithms,
                        options={"verify_signature": False})
    print("---------------------------------------------------------")
    print(claims)
    print(claims['qsh'])
    print("---------------------------------------------------------")
    print(hash_url(http_method,url))
    # if claims['qsh'] != hash_url(http_method, url):
    #     raise DecodeError('qsh does not match')
    shared_secret = 'ATCObQrv98enQA7YN6wo6GrDqqQCiDO4rQDdZCdAfHVJURZW9Peil5UKlg'
    # verify shared secret
    print(":::::::::::;audience::::::")
    print(claims.get('aud'))
    jwt.decode(
        token, algorithms=algorithms, verify=False)
        # audience=claims.get('aud'),
        # key = shared_secret,
        # algorithms=algorithms,
        # leeway=leeway,options={'verify_aud': False})

    # return client key, claims
    AuthResult = collections.namedtuple('AuthResult',
                                        ['client_key', 'claims'])
    print("Auth Result")
    print(AuthResult)
    return AuthResult(claims['iss'], claims)

class Authenticator(object):
    """An abstract base class for authenticating Atlassian Connect requests.

    Subclasses *must* implement the `get_shared_secret` method.

    Example:
        Subclass this abstract base class to provide authentication to an
        Atlassian Connect Addon.

        import atlassian_jwt

        class MyAddon(atlassian_jwt.Authenticator):
            def __init__(self, tenant_info_store):
                super(MyAddon, self).__init__()
                self.tenant_info_store = tenant_info_store

            def get_shared_secret(self, client_key):
                tenant_info = self.tenant_info_store.get(client_key)
                return tenant_info['sharedSecret']

        mauth = MyAddon(tenant_info_store)
        try:
            client_key, claims = mauth.authenticate(http_method, url, headers)
            # authentication succeeded
        except atlassian_jwt.DecodeError:
            # authentication failed
            pass
    """
    # __metaclass__ = abc.ABCMeta

    def __init__(self, algorithms=('HS256',), leeway=90, token=None):
        self.algorithms = algorithms
        self.leeway = leeway
        self.token = token

    # @abc.abstractmethod
    # def get_shared_secret(self, client_key):
    #     shared_secret = 'ATCObQrv98enQA7YN6wo6GrDqqQCiDO4rQDdZCdAfHVJURZW9Peil5UKlg'
    #     return shared_secret
        # """Get the shared secret associated with the client key.
        #
        # Subclasses of this abstract base class *must* implement this method.
        #
        # Use the client key to retrieve the shared secret (presumably) from a
        # persistent store of which this abstract base class does not need to
        # know the details.
        #
        # This is the shared secret that was used to sign the JWT token and can
        # be used to verify its authenticity.
        #
        # Args:
        #     client_key (string): client key
        #
        # Returns:
        #     string: shared secret used to sign the JWT token
        # """
        # raise NotImplementedError

    def authenticate(self, http_method, url, token):
        """Extract the JWT token from the `Authorization` header, or if not
        found there then the `jwt` query parameter.

        Args:
            http_method (string): HTTP method

            url (string): URL

            headers (dict): incoming request headers. The header name
                `Authorization` is case-insensitive. The token type `JWT` in
                the `Authorization` header is case-insensitive.

        Returns:
            a named tuple of: the client key (the `iss` claim from the JWT
                token) & claims (accessible via .client_key & .claims)

        Raises:
            DecodeError: If neither `headers` nor the query parameters in
                `url` contain a JWT token. Or if `qsh` claim does not match
                expected value.

        .. _Exposing a service:
           https://developer.atlassian.com/static/connect/docs/latest/concepts/authentication.html#exposing
        """
        # token = self._get_token(
        #     headers=headers,
        #     query_params=parse_query_params(url))

        claims = jwt.decode(token, algorithms=self.algorithms,
                            options={"verify_signature": False})
        if claims['qsh'] != hash_url(http_method, url):
            raise DecodeError('qsh does not match')

        # verify shared secret
        jwt.decode(
            token,
            audience=claims.get('aud'),
          #  key=self.get_shared_secret(claims['iss']),
            key=self.shared_secret,
            algorithms=self.algorithms,
            leeway=self.leeway)

        # return client key, claims
        AuthResult = collections.namedtuple('AuthResult',
                                            ['client_key', 'claims'])
        print("Auth Result")
        print(AuthResult)
        return AuthResult(claims['iss'], claims)

    @staticmethod
    def _get_token(headers=None, query_params=None):
        if headers:
            for name, value in headers.items():
                print("-------Name---------")
                print(name)
                print(value)
                if name.lower() == 'authorization':
                    print("-------Name Auth---------")
                    print(name)
                    value = value["Authorization"]
                    parts = value.split()
                    if len(parts) > 1 and parts[0].lower() == 'jwt':
                        return parts[1]

        if query_params and 'jwt' in query_params:
            value = query_params['jwt']
            return value if isinstance(value, str) else value[0]

        raise DecodeError('JWT token not found')

    # def create_token(self, uri, method='GET'):
    #     return security.create_token(self, uri, method)