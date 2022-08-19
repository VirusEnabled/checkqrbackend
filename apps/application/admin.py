from django.contrib import admin
from . import models

admin.site.register(models.Application)
admin.site.register(models.ApplicationConfiguration)
admin.site.register(models.ApplicationUrl)
admin.site.register(models.ApplicationTag)