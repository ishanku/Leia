from Roja.Totes.core.utils.logger import *

class decoder:
    algorithms = ('HS256',)
    leeway = 90
    key = get_client_key(uri)
    shared_secret = get_shared_secret(key)
    opts = {"start_at": 0}
    uri_search_pattern = '/rest/api/3/search?%(get_opts)s&startAt=%(start_at)s&maxResults=%(max_results)s'
    get_opts = query_builder()

    def decode_claims(self, token, algorithms = self.algorithms):
        claims = jwt.decode(token, algorithms=algorithms,
                            options={"verify_signature": False})
        return claims