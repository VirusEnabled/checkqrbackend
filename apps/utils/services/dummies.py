"""
this file is to have a dummy objects
that we can use in order to mock properties
and objects for testing and application creation.

"""
class DummyConfig(object):
    """
    this is a dummy configuration
    in order to make sure the app can
    use properly the implementation.
    """
    def __init__(self) -> None:
        self.timeout = 40
        self.uses_main_credentials = False
        self.application_token = ''
        self.application_secret = ''
        self.base_url =  ''