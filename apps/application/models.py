from django.db import models
from apps.utils.models import BaseModel
import apps.application.services as services


class Application(BaseModel,
                  services.ApplicationService,
                  services.ApplicationApiLoader):

    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class ApplicationConfiguration(BaseModel,
                               services.ConfigurationService):
    application = models.OneToOneField(Application,
                                       on_delete=models.CASCADE,
                                       related_name='configuration')
    base_url = models.URLField()
    application_token = models.CharField(max_length=200,
                                         null=True,
                                         blank=True)
    application_secret = models.CharField(max_length=200,
                                          null=True,
                                          blank=True)
    timeout = models.IntegerField(default=40)
    implements_input_search = models.BooleanField(default=False)
    implements_checkout = models.BooleanField(default=False)
    needs_user_secret = models.BooleanField(default=False)
    uses_main_credentials = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Config for App: {self.application}"


class ApplicationUrl(BaseModel,
                     services.ApplicationUrlService):
    name = models.CharField(max_length=200)
    application = models.ForeignKey(Application,
                                    on_delete=models.CASCADE,
                                    related_name='urls')
    description = models.TextField(blank=True)
    url = models.CharField(max_length=500)
    requires_additional_formating = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
