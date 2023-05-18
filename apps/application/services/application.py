from apps.application.enums import HttpMethods
# import requests
from apps.utils.services.base_api import BaseApi
from apps.utils.services import dummies
from django.conf import settings
# this service might become a stand alone
# rather than a helper
class ApplicationApiLoader(BaseApi):
    """
    implements the searches
    on the different applications
    to search the qr information
    gathered by the reader.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setup(self):
        """
        overrides the main url
        and sets all of the 
        required information
        to start it up
        """
        self.config = self.load_config()
        self.timeout = self.config.timeout
        self.methods = {
            HttpMethods.get: self._get,
            HttpMethods.post: self._post,
            HttpMethods.put: self._put,
            HttpMethods.delete: self._delete
        }
        self.urls_base = self.preload_urls()
        self.headers = self.get_header()

    def load_config(self):
        """
        gets the configuration
        based on the required
        parameters.

        this is to avoid issues when the 
        application is not created.
        :returns: object
        """
        return (self.configuration
                if hasattr(self, 'configuration')
                else self.gen_config_dummy())

    def gen_config_dummy(self):
        """
        creates an empty configuration
        for testing and application
        creation purposes
        :return: object
        """
        configuration = dummies.DummyConfig()
        return configuration

    def gen_credentials_dummy(self):
        """
        generates a dummy
        credential for the 
        testing in case it's needed
        """

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
                else validator.get_credentials() if not 
                self.configuration.uses_jwt_validation else
                self.get_jwt_credentials(validator)) 

    def get_jwt_credentials(self, validator=None):
        """
        this is a method that
        gets the credentials from
        the remote app and saves it in
        redis

        it verifies if the token is 
        in memory if so it just returns
        it else it goes remotely and
        set the new one
        """
        key_finder = 'JWTTOKEN'
        key = validator.uuid
        existing = settings.REDIS_HANDLER.get_qr_validator_jwt(key)
        result = {}
        # if existing['status']:
        #     result['Authorization'] = f"Bearer {existing['data']['access']}"
        # else:
        # we look for it remotely.
        get_token_url =(self.urls.
                        filter(name__contains=key_finder).
                        last().name)
        data = {
            'username': validator.credentials.remote_username,
            'password': validator.credentials.remote_password
        }
        url = self.urls_base[get_token_url]
        headers=self.headers
        params = {}
        url_param = None
        response = (self.methods['POST'](url=url['url_go'],
                                headers=headers,
                                data=data,
                                url_param=url_param,
                                params=params,
                                param=params))
        if response['status']:
            resp = response['response']
            response_data = (resp['data']
                            if 'data' in 
                            resp.keys() else resp)
            staged =(settings.
                        REDIS_HANDLER.
                        set_qr_validator_jwt(key, response_data))
            result['Authorization'] = f"Bearer {response_data['access']}"
        else:
            raise Exception(response['response'])            
        return result

    # need to finish this method and implement it.
    def refresh_jwt_credentials(self, validator=None):
        """
        this is a method that
        gets the credentials from
        the app and saves it in
        redis

        it refreshes straight
        forward and updates 
        the redis file
        then returns the new token.
        """
        key_finder = 'JWTREFRESH'


    def get_main_credentials(self):
        """
        gets the main credentials
        based on the configurations
        :returns: dict
        """
        initial_header  = {'Authorization': 
                           self.config.
                           application_token
                           }

        # might need modification based on changes in apps
        if self.config.application_secret:
            initial_header['Application'] = (self.config.
                                             application_secret)
        return initial_header
    
    # needs to be updated
    def build_url_params(self, url_name, qr_data):
        """
        builds the url params
        in case there's any additional
        parameters for the url.
        :params:
            kwargs: dict.
        :returns: dict
        """
        result = {}

        return result

    def perform_request(self, url_name,
                        validator, qr_data,
                        param_url=None):
        """
        makes the validation of the 
        url provided and the qr_data
        to the given url in the app.

        :params:
            url_name: str: name of the url:
            identifier has the http method to use
            validator: validator_object
            qr_data: dict: data coming from the frontend
            param_url: str: could be a 
            parameter to add to the link
            ike an ID or a unique key
        :returns: dict: response from the service
        """
        url = self.urls_base[url_name]
        credentials = (self.
                        get_credentials(validator=
                                        validator))
        headers = (self.
                   attach_credentials_to_headers(
                       credentials=credentials))
        headers = self.headers
        data = qr_data
        url_param = (param_url
                    if not url['url'].requires_additional_formating
                    else data['qr_data'])
        params = self.build_url_params(url_name, qr_data)
        response = (self.
                    methods[url['url'].
                    http_method](url=url['url_go'],
                                 headers=headers,
                                 data=data,
                                 url_param=url_param,
                                 params=params,
                                 param=params))
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
        return f"{self.config.base_url}{url.url}"

    