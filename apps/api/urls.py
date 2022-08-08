from django.urls import path
import views

app_name = 'apps.api'

url_patterns = [
    path('', view=views.HomeApiView.as_view(), name='home')
]