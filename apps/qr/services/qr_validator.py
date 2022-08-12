

class ValidatorService(object):
    """
    application service
    to hold all functionalities
    for the application
    """

    def get_logged_in_config(self):
        """
        loads all of the information required
        to load the user based on the needed
        implementation in order to get the rest
        :returns: dict
        """
        return {
                'urls': self.build_urls_for_frontend(),
                'needs_checkout': self.application.
                configuration.implements_checkout,
                'needs_input_search': self.application.
                configuration.implements_input_search,
                }
    
    def build_urls_for_frontend(self):
        """
        builds the urls 
        based on the application.
        :return: list
        """
        result = [{'name': url.name,
                   'requires_additional_format': 
                   url.requires_additional_formating} 
                  for url in self.application.
                    urls.all()]


        return result