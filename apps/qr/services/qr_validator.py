

class ValidatorService(object):
    """
    application service
    to hold all functionalities
    for the application
    """

    @property
    def token(self):
        """
        shortcut to the
        token for the user
        :returns: string
        """
        return self.user.auth_token.key

    def get_credentials(self):
        """
        gets the credentials
        based on the saved records
        :returns: dict
        """
        initial_header  = {'Authorization': self.credentials.token,
                           }
        # might need modification based on changes in apps
        if self.credentials.secret:
            initial_header['Application'] = self.credentials.secret

        return initial_header


    def change_token(self):
        """
        changes the token
        for the user so that they 
        can have a new token every
        time they login.
        :returns: None
        """
        from rest_framework.authtoken.models import Token
        user_token = self.user.auth_token
        new_key = user_token.generate_key()
        user_token.delete()
        Token.objects.create(user=self.user)

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