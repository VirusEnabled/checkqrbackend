from django.urls import path
from . import views

app_name = 'apps.api'

urlpatterns = [
    path('', view=views.HomeApiView.as_view(), name='home')
]