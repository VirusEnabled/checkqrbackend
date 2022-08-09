from django.db import models
from apps.utils.models import BaseModel
import apps.qr.services as services
from django.contrib.auth.models import User
from apps.application.models import (
    Application,
    ApplicationUrl
)
from rest_framework.authtoken.models import Token
from typing import *


class ValidatorCredential(BaseModel):
    name = models.CharField(max_length=400,
                            null=True,
                            blank=True)
    application = models.ForeignKey(Application,
                                    on_delete=models.CASCADE,
                                    related_name='registered_credentials')
    token =  models.CharField(max_length=400)
    secret = models.CharField(max_length=400,
                              null=True,
                              blank=True)

    def __str__(self) -> str:
        return f'{self.application.name}\'s credentials'


class QRValidator(BaseModel, services.ValidatorService):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='qr_validator')
    application = models.ForeignKey(Application,
                                    on_delete=models.CASCADE,
                                    related_name='qr_validator')
    credentials = models.ForeignKey(ValidatorCredential,
                                     on_delete=models.CASCADE,
                                     related_name='validators')
    def __str__(self) -> str:
        return f"QRValidator for {self.user.username}"

    def save(self,*args, **kwargs) -> None:
        if not self.pk:
            (Token.
             objects.
             get_or_create(user=self.user)[0])

        return super().save(*args, **kwargs)


class QR(BaseModel, services.QRService):
    code = models.TextField()
    validator = models.ForeignKey(QRValidator,
                                  on_delete=models.CASCADE,
                                  related_name='qr_read')
    application = models.ForeignKey(Application,
                                    on_delete=models.CASCADE,
                                    related_name='qr_logs')
    url = models.ForeignKey(ApplicationUrl,
                            on_delete=models.CASCADE,
                            related_name='qr_accessed')
    response = models.TextField()
    response_code = models.IntegerField()


    def __str__(self) -> str:
        return f"Log for QR: {self.code}"
