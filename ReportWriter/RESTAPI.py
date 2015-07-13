import requests

class RESTAPI:

    ENHANCED_CWE_BASE_URL = 'http://localhost:9000/api/v1'
    ENHANCED_CWE_API_KEY = 'f9a62b1c40ff2a42325cbadec77cfc2351807898'

    @staticmethod
    def get_header():
        return {'Authorization': RESTAPI.ENHANCED_CWE_API_KEY}

    @staticmethod
    def get_cwes_for_description(description):
        payload = {'text': description}
        url_string = '%s/cwe/text_related' % RESTAPI.ENHANCED_CWE_BASE_URL
        r = requests.get(url_string, params=payload, headers=RESTAPI.get_header())
        print(r.content)
