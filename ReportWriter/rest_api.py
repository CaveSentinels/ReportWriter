import requests

class rest_api:

    # Base URL of the Enhanced CWE Application
    ENHANCED_CWE_BASE_URL = 'http://localhost:9000/api/v1'

    # API Key
    ENHANCED_CWE_API_KEY = 'Token f9a62b1c40ff2a42325cbadec77cfc2351807898'

    @staticmethod
    def get_header():
        '''
        Creates a dictionary of the things to be passed in the REST requests header
        :return: A dictionary containing the API key
        '''
        return {'Authorization': rest_api.ENHANCED_CWE_API_KEY}

    @staticmethod
    def process_response(response):
        '''
        This method process the response for errors or success
        :param response: Response object that's been returned from the server
        :return: A dictionary containing the following three key-values:
         success: A boolean value representing whether request to the server was successful or not
         msg: A string containing a descriptive message about what happened with the request
         obj: Any additional object (generally the JSON object) if some data is to be returned to the caller.
        '''
        success = False
        msg = None
        obj = None
        if response.status_code == requests.codes.unauthorized:
            # Authentication Failure
            msg = 'Authentication Failure. All requests must be authenticated with a valid API Key. ' \
                  'Please contact the system administrator. Additional error details are: %s' % response.content
        elif response.status_code == requests.codes.bad:
            # Bad Request
            msg = 'There is something wrong in the request. Please check all your inputs correctly.' \
                  'Additional error details are: %s' % response.content
        elif response.status_code == requests.codes.server_error:
            # Server Error occurred.
            msg = 'Some error has occurred on the server. Please try after some time!' \
                  'Additional error details are: %s' % response.content
        elif response.status_code == requests.codes.ok:
            # Successful
            success = True
            msg = 'Success'
            if response.headers.get('content-type') == 'application/json':
                # If the response is of type JSON, set the obj
                obj = response.json()

        return {'success': success, 'msg': msg, 'obj': obj}

    @staticmethod
    def get_cwes_for_description(description):
        '''
        This method makes a REST call to Enhanced CWE system to get the related CWEs for the report description
        :param description: A string which is the description of the report
        :return: Returns a dictionary containing whether the request was successful or not. If the request was not
                 successful, the dictionary also contains the descriptive error message. If the request was successful,
                 the dictionary also contains the list of the CWEs returned from the Enhanced CWE application
        '''
        payload = {'text': description}
        url_string = '%s/cwe/text_related' % rest_api.ENHANCED_CWE_BASE_URL
        response = requests.get(url_string, params=payload, headers=rest_api.get_header())
        return rest_api.process_response(response)

    @staticmethod
    def get_cwes_with_search_string(search_string, offset, limit):
        '''
        This method makes a REST call to Enhanced CWE system to search the cwe based on one of the following arguments:
        :param search_string: string to be searched in code and name
        :param offset: An offset value indicating the id of the CWE where to start search from
        :param limit: Limit indicating the maximum number of results to return
        :return: Returns a dictionary containing whether the request was successful or not. If the request was not
                 successful, the dictionary also contains the descriptive error message. If the request was successful,
                 the dictionary also contains the list of the CWEs returned from the Enhanced CWE application
        '''
        payload = {'search_str': search_string,
                   'offset': offset,
                   'limit': limit}
        url_string = '%s/cwe/search_str' % rest_api.ENHANCED_CWE_BASE_URL
        response = requests.get(url_string, params=payload, headers=rest_api.get_header())
        return rest_api.process_response(response)

    @staticmethod
    def get_cwes(code, name_search_string, offset, limit):
        '''
        This method makes a REST call to Enhanced CWE system to search the cwe based on one of the following arguments:
        :param code: CWE code
        :param name_search_string: A string to search in the name of the CWEs
        :param offset: An offset value indicating the id of the CWE where to start search from
        :param limit: Limit indicating the maximum number of results to return
        :return: Returns a dictionary containing whether the request was successful or not. If the request was not
                 successful, the dictionary also contains the descriptive error message. If the request was successful,
                 the dictionary also contains the list of the CWEs returned from the Enhanced CWE application
        '''
        payload = {'code': code,
                   'name_contains': name_search_string,
                   'offset': offset,
                   'limit': limit}
        url_string = '%s/cwe/all' % rest_api.ENHANCED_CWE_BASE_URL
        response = requests.get(url_string, params=payload, headers=rest_api.get_header())
        return rest_api.process_response(response)

    @staticmethod
    def get_misuse_cases(cwe_codes):
        '''
        This method makes a REST call to Enhanced CWE system to get the list of misuse cases related a list of CWEs
        :param cwe_codes: A comma separated string of CWE codes for which misuse cases are needed
        :return: Returns a dictionary containing whether the request was successful or not. If the request was not
                 successful, the dictionary also contains the descriptive error message. If the request was successful,
                 the dictionary also contains the list of the misuse cases returned from the Enhanced CWE application
        '''
        payload = {'cwes': str(cwe_codes)}
        url_string = '%s/misuse_case/cwe_related' % rest_api.ENHANCED_CWE_BASE_URL
        response = requests.get(url_string, params=payload, headers=rest_api.get_header())
        return rest_api.process_response(response)

    @staticmethod
    def get_use_cases(misuse_case_ids):
        '''
        This method makes a REST call to Enhanced CWE system to get the list of use cases related a list of misuse cases
        :param misuse_case_ids: A comma separated string of Misuse case ids for which use cases are needed
        :return: Returns a dictionary containing whether the request was successful or not. If the request was not
                 successful, the dictionary also contains the descriptive error message. If the request was successful,
                 the dictionary also contains the list of the use cases returned from the Enhanced CWE application
        '''
        payload = {'misuse_cases': str(misuse_case_ids)}
        url_string = '%s/use_case/misuse_case_related' % rest_api.ENHANCED_CWE_BASE_URL
        response = requests.get(url_string, params=payload, headers=rest_api.get_header())
        return rest_api.process_response(response)

    @staticmethod
    def save_muos_to_enhanced_cwe(cwe_codes, misuse_case_description, use_case_description, osr_description):
        '''
        This method makes a REST call to Enhanced CWE system to save the misuse case, use case and overlooked security
        requirements to the Enhanced CWE system
        :param cwe_codes: A comma separated string of CWE codes
        :param misuse_case_description: A string which is the description of the misuse case
        :param use_case_description: A string which is the description of the use case
        :param osr_description: A string representing the description of the osr
        :return: Returns a dictionary containing whether the request was successful or not. If the request was not
                 successful, the dictionary also contains the descriptive error message.
        '''
        payload = {'cwes': str(cwe_codes),
                   'muc': str(misuse_case_description),
                   'uc': str(use_case_description),
                   'osr': str(osr_description)}
        url_string = '%s/custom_muo/save' % rest_api.ENHANCED_CWE_BASE_URL
        response = requests.post(url_string, data=payload, headers=rest_api.get_header())
        return rest_api.process_response(response)

