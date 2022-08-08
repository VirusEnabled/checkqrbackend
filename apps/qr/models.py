from django.db import models
from apps.utils.models import BaseModel
import apps.qr.services as services


class ValidatorCredential(BaseModel):
    application = models.ForeignKey('Application',
                                    on_delete=models.CASCADE,
                                    related_name='registered_credentials')
    token =  models.CharField(max_length=400)
    secret = models.CharField(max_length=400,
                              null=True,
                              blank=True)

    def __str__(self) -> str:
        return f'{self.validator}\'s credentials'


class QRValidator(BaseModel, services.ValidatorService):
    user = models.OneToOneField('User',
                                on_delete=models.CASCADE,
                                related_name='qr_validator')
    application = models.ForeignKey('Application',
                                    on_delete=models.CASCADE,
                                    related_name='qr_validator')
    credentials = models.ForeignKey(ValidatorCredential,
                                     on_delete=models.CASCADE,
                                     related_name='validators')
    def __str__(self) -> str:
        return f"QRValidator for {self.user.username}"

class QR(BaseModel, services.QRService):
    code = models.TextField()
    validator = models.ForeignKey(QRValidator,
                                  on_delete=models.CASCADE,
                                  related_name='qr_read')
    application = models.ForeignKey('Application',
                                    on_delete=models.CASCADE,
                                    related_name='qr_logs')
    url = models.ForeignKey('ApplicationUrl',
                            on_delete=models.CASCADE,
                            related_name='qr_accessed')
    response = models.TextField()
    response_code = models.IntegerField()


    def __str__(self) -> str:
        return f"Log for QR: {self.code}"