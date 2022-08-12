from django.urls import path
from . import views

app_name = 'apps.api'

urlpatterns = [
    path('',
         view=views.HomeApiView.as_view(),
         name='home'),
    path('accounts/login/',
         view=views.LoginQrValidator.as_view(),
         name='login_user'),
    path('accounts/logout/', view=views.LogOutQrValidator.as_view(),
         name='logout_user')
]