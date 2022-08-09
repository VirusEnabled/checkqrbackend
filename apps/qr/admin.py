from django.contrib import admin
from . import models

admin.site.register(models.QR)
admin.site.register(models.QRValidator)
admin.site.register(models.ValidatorCredential)