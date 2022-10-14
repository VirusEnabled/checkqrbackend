from apps.application.enums import HttpMethods

class ApplicationUrlService(object):
    """
    service used to manage the methods
    to apply to the url models.
    """
    
    @property
    def http_method(self) -> str:
        """
        identifies the http
        method based on the 
        name assigned to the url.
        :returns: str
        """
        result = (HttpMethods.delete if HttpMethods.delete in self.name
                  else HttpMethods.post 
                  if HttpMethods.post in self.name
                  else HttpMethods.put 
                  if HttpMethods.put in self.name else
                  HttpMethods.get)
        
        return result
        
    