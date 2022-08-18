from apps.application.enums import HttpMethods
# import requests
from apps.utils.services.base_api import BaseApi


class ApplicationApiLoader(BaseApi):
    """
    implements the searches
    on the different applications
    to search the qr information
    gathered by the reader.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    # def get_header(self):
    #     """
    #     gets the header
    #     for all requests
    #     required in order to manage
    #     the implementation of bookeo API
    #     returns: dict
    #     """
    #     return {
    #         'Content-Type': 'application/json'
    #     }

    def setup(self):
        """
        overrides the main url
        and sets all of the 
        required information
        to start it up
        """
        self.timeout = self.configuration.timeout
        self.methods = {
            HttpMethods.get: self._get,
            HttpMethods.post: self._post,
            HttpMethods.put: self._put,
            HttpMethods.delete: self._delete
        }
        self.urls_base = self.preload_urls()
        self.headers = self.get_header()

    def preload_urls(self):
        """
        loads all of the urls
        registered to the site
        based on the url name
        :returns: Dict
        """
        return { url.name: {'url_go': self.format_url(url),
                            'url': url}
                 for url in self.urls.all()
                 }

    def get_credentials(self, validator=None):
        """
        generates the credentials needed
        in order to authorize the access to
        the platform it's trying to access
        :params:
            validator: a qr_validator object which
            is used based on whether the user
            needs to use its own authentication
            or the main based on the configurations

        :returns: dict
        """
        return (self.get_main_credentials()
                if self.configuration.uses_main_credentials
                else validator.get_credentials())    

    def update_params(self, params, validator=None):
        """
        appends the credential
        keys to make the request work.
        :params:
            params: dict. the request params.
            validator: validator object to pull credentials
        returns: dict
        """
        if validator:
            credentials = self.get_credentials(validator)
            for k in credentials.keys():
                params[k] = credentials[k]
        return params

    def get_main_credentials(self):
        """
        gets the main credentials
        based on the configurations
        :returns: dict
        """
        initial_header  = {'Authorization': 
                           self.configuration.
                           application_token
                           }

        # might need modification based on changes in apps
        if self.configuration.application_secret:
            initial_header['Application'] = (self.
                                             configuration.
                                             application_secret)
        return initial_header

    def perform_request(self, url_name, validator, qr_data):
        """
        makes the validation of the 
        url provided and the qr_data
        to the given url in the app.

        :params:
            url_name: str: name of the url:
            identifier has the http method to use
            validator: validator_object
            qr_data: dict: data coming from the frontend
        :returns: dict: response from the service
        """
        url = self.urls_base[url_name]
        headers = self.update_params(self.headers,
                                     validator=validator)
        data = qr_data
        url_param = None  # this will have to be specified in the url
        params = {}
        # import ipdb; ipdb.set_trace()
        response = (self.
                    methods[url['url'].
                    http_method](url=url['url_go'],
                                 headers=headers,
                                 data=data,
                                 url_param=url_param,
                                 params=params,
                                 param=params,
                                 validator=validator))

        self.log_qr_reading(qr_data=data, url=url['url'],
                            response_code=response['status_code'],
                            response=response['response'],
                            validator=validator)
        return response

    def log_qr_reading(self, qr_data, url,
                       response, response_code,
                       validator):
        """
        logs the reading for the qr made
        :params:
            qr_data: str: data read
            url: application url object
            response: json: response from the external app
            response_code: response code from external app
            validator: validator user who performed the reading
        :returns: None
        """
        from apps.qr.models import QR
        QR.objects.create(application=self,
                          validator=validator,
                          code=qr_data,
                          url=url,
                          response=response.__str__(),
                          response_code=response_code)

    
    # def _get(self, **kwargs):
    #     """
    #     performs the GET method.

    #     :params:
    #         url_name: url to perform acction.
    #         params: dict: params required for the method.
    #         url_param: this is a param that will be placed in the url
    #         rather than passed as paramter keys.
    #     :returns: dict
    #     """
    #     import ipdb; ipdb.set_trace()
    #     url_name = kwargs['url_name']
    #     url_param = kwargs['url_param']
    #     headers = kwargs['headers']
    #     result = {}
    #     url = self.urls_base.get(url_name)
    #     if url_param:
    #         url = f"{url}{url_param}/"
    #     params = self.update_params(params)
    #     headers =  headers if headers else self.headers
    #     response = requests.get(url,
    #                             headers=self.headers,
    #                             params=params,
    #                             timeout=self.timeout)
    #     result['status'] = response.ok
    #     result['response'] = response.json()
    #     result['status_code'] = response.status_code

    #     return result

    # def _post(self, **kwargs):
    #     """
    #     performs the POST method.

    #     :params:
    #         url_name: url to perform acction.
    #         data: dict: params required for the method.
    #         url_param: specific param to be passed in
    #         case of need directly in the url.
    #         url_params: dict if passed
    #         it provides all query params to be updated

    #     :returns: dict
    #     """
    #     url_name = kwargs['url_name']
    #     url_param = kwargs['url_param']
    #     headers = kwargs['headers']
    #     data = kwargs['data']
    #     url_params = kwargs['param']
    #     result = {}
    #     url = self.urls_base.get(url_name)
    #     validator = kwargs.get('validator', None)
    #     if url_param:
    #         url = f"{url}{url_param}/"
    #     credentials = self.get_credentials(validator=validator)
    #     if url_params:
    #         credentials = self.update_params(url_params,
    #                                          validator=validator)
    #     dt = data
    #     headers = headers if headers else self.headers
    #     response = requests.post(url,
    #                              headers=self.headers,
    #                              json=dt,
    #                              params=credentials,
    #                             timeout=self.timeout)
    #     result['status'] = response.ok
    #     result['response'] = response.json()
    #     result['status_code'] = response.status_code

    #     return result

    # def _put(self, **kwargs):
    #     """
    #     performs the PUT method.

    #     :params:
    #         url_name: url to perform acction.
    #         params: dict: params required for the method.
    #         url_param: specific param to be passed in
    #         case of need directly in the url.
    #     :returns: dict
    #     """
    #     url_name = kwargs['url_name']
    #     url_param = kwargs['url_param']
    #     headers = kwargs['headers']
    #     data = kwargs['data']
    #     result = {}
    #     validator = kwargs.get('validator', None)
    #     url = self.urls_base.get(url_name)
    #     headers = headers if headers else self.headers

    #     if url_param:
    #         url = f"{url}{url_param}/"
    #     credentials = self.get_credentials(validator=validator)
    #     response = requests.put(url,
    #                             headers=self.headers,
    #                             json=data,
    #                             params=credentials,
    #                             timeout=self.timeout)
    #     result['status'] = response.ok
    #     result['response'] = response.json()
    #     result['status_code'] = response.status_code

    #     return result

    # def _delete(self, **kwargs):
    #     """
    #     performs the DELETE method.

    #     :params:
    #         url_name: url to perform acction.
    #         params: dict: params required for the method.
    #         url_param: specific param to be passed in
    #         case of need directly in the url.
    #     :returns: dict
    #     """
    #     url_name = kwargs['url_name']
    #     url_param = kwargs['url_param']
    #     headers = kwargs['headers']
    #     data = kwargs['data']
    #     result = {}
    #     headers =  headers if headers else self.headers
    #     url = self.urls_base.get(url_name)
    #     if url_param:
    #         url = f"{url}{url_param}/"
    #     credentials = self.get_credentials()
    #     response = requests.delete(url,
    #                                headers=self.headers,
    #                                json=data,
    #                                params=credentials,
    #                                timeout=self.timeout)
    #     result['response'] = {'message': "the object was deleted successfully"
    #                           if not response.text else response.text}
    #     result['status_code'] = response.status_code

    #     return result



class ApplicationService(object):
    """
    application service
    to hold all functionalities
    for the application
    """

    def load_url(self, url_name):
        """
        gets the url from the
        application.
        :params:
            url_name: url name:str
        :returns: application url object
        """
        return self.urls.get(name=url_name)

    def format_url(self, url):
        """
        prepares the url for the 
        request to validate the platform

        :params:
            url: application url object
        :returns: str
        """
        return f"{self.configuration.base_url}{url.url}"

    