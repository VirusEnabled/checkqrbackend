from datetime import datetime
import requests
from django.conf import settings
from simplejson.errors import JSONDecodeError
# needs to be fixed because we need to use this helper
# in order to implement what we need for the project.
class BaseApi(object):
    """
    this is a base app
    that implements all
    type of wrappers and 
    implements the basic
    methods
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        here we're setting the base
        information, for now we're not
        passing anything and only fetching
        the env variables for the api key
        and secret.

        the object is going to be the based
        object and we're going to interact
        with all of the properties
        based on the code asked in the kwargs.
        but if the secret key is not now then we
        just use the given api_key to
        identify the property.
        """
        self.args = args
        self.kwargs = kwargs
        self.timeout = 40
        self.setup()

    def setup(self):
        """
        sets all of the
        variables required 
        to make the service work.
        """
        raise NotImplementedError

    def attach_credentials_to_headers(self, credentials):
        """
        attaches the credentials
        to the headers
        :params:
            credentials: dict: credentials setup.
        :returns: None
        """
        for key, val in credentials.items():
            self.headers[key] = val

    def update_params(self, params, **kwargs):
        """
        updates the params for the request
        keys to make the request work.
        :params:
            params: dict. the request params.
            kwargs: dict: kwargs for the params
        returns: dict
        """
        for k in kwargs.keys():
            params[k] = kwargs[k]
        return params

    def get_credentials(self, **kwargs):
        """
        gets the key and secret
        values for the authentication
        of the application.
        returns: dict
        """
        raise NotImplementedError

    def get_header(self):
        """
        gets the header
        for all requests
        required in order to manage
        the implementation of bookeo API
        returns: dict
        """
        return {
            'Content-Type': 'application/json'
        }

    def process_response(self, response, method_called):
        """
        processes the 
        response in order to have
        the implementation cleaned 
        so that we can avoid errors
        coming from the site in the parsing
        or json decoding.
        :params:
            response: requests response.
            method_called: str: tag for the 
            method. this is used in order to 
            trigger the right error message.
        :return: dict
        """
        result = {}
        error_tags = {
           'json_error': 'internal_error_parsing',
           'no_found': 'internal_not_found',
           'internal_error':'internal_error'
        }
        try:
            result = response.json()

        except JSONDecodeError:
            result = {'error': error_tags['json_error']
                               if response.status_code == 500 
                               else error_tags['not_found']
                               if response.status_code == 404 else
                               error_tags['internal_error']}

        return result


    def _get(self, **kwargs):
        """
        performs the GET method.

        :params:
            url_name: url to perform acction.
            params: dict: params required for the method.
            url_param: this is a param that will be placed in the url
            rather than passed as paramter keys.
        :returns: dict
        """
        TAG = 'GET'
        url = kwargs['url']
        url_param = kwargs['url_param']
        headers = kwargs['headers']
        params = kwargs['params']
        data = kwargs.get('data', {})
        result = {}
        if url_param:
            url = f"{url}{url_param}/"
        params = self.update_params(params)
        headers =  headers if headers else self.headers
        response = requests.get(url,
                                headers=self.headers,
                                params=params,
                                timeout=self.timeout,
                                json=data)
        response_json = self.process_response(response, TAG)
        result['status'] = response.ok
        result['response'] = (response_json if 'data'
                              in response_json.keys()
                              else {'data': response_json})
        result['status_code'] = response.status_code

        return result

    def _post(self, **kwargs):
        """
        performs the POST method.

        :params:
            url_name: url to perform acction.
            data: dict: params required for the method.
            url_param: specific param to be passed in
            case of need directly in the url.
            url_params: dict if passed
            it provides all query params to be updated

        :returns: dict
        """
        TAG = 'POST'
        url = kwargs['url']
        url_param = kwargs['url_param']
        headers = kwargs['headers']
        data = kwargs['data']
        url_params = kwargs['param']
        result = {}
        parameters = {}
        if url_param:
            url = f"{url}{url_param}/"

        if url_params:
            parameters = self.update_params(url_params)
        headers = headers if headers else self.headers
        response = requests.post(url,
                                 headers=self.headers,
                                 json=data,
                                 params=parameters,
                                timeout=self.timeout)
        response_json = self.process_response(response, TAG)
        result['status'] = response.ok
        result['response'] = response_json
        result['status_code'] = response.status_code

        return result

    def _put(self, **kwargs):
        """
        performs the PUT method.

        :params:
            url_name: url to perform acction.
            params: dict: params required for the method.
            url_param: specific param to be passed in
            case of need directly in the url.
        :returns: dict
        """
        TAG = 'PUT'
        url = kwargs['url']
        url_param = kwargs['url_param']
        headers = kwargs['headers']
        data = kwargs['data']
        url_params = kwargs['param']
        result = {}
        parameters = {}
        if url_param:
            url = f"{url}{url_param}/"

        if url_params:
            parameters = self.update_params(url_params)
        headers = headers if headers else self.headers
        response = requests.put(url,
                                 headers=self.headers,
                                 json=data,
                                 params=parameters,
                                timeout=self.timeout)
        response_json = self.process_response(response, TAG)
        result['status'] = response.ok
        result['response'] = response_json
        result['status_code'] = response.status_code

        return result

    def _delete(self, **kwargs):
        """
        performs the DELETE method.

        :params:
            url_name: url to perform acction.
            params: dict: params required for the method.
            url_param: specific param to be passed in
            case of need directly in the url.
        :returns: dict
        """
        TAG = 'POST'
        url = kwargs['url']
        url_param = kwargs['url_param']
        headers = kwargs['headers']
        data = kwargs['data']
        url_params = kwargs['param']
        result = {}
        parameters = {}
        if url_param:
            url = f"{url}{url_param}/"

        if url_params:
            parameters = self.update_params(url_params)
        headers = headers if headers else self.headers
        response = requests.delete(url,
                                 headers=self.headers,
                                 json=data,
                                 params=parameters,
                                timeout=self.timeout)
        response_json = self.process_response(response, TAG)
        result['status'] = response.ok
        result['response'] = response_json
        result['status_code'] = response.status_code

        return result
