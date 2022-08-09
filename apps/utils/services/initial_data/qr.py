from apps.qr import models
from django.contrib.auth.hashers import make_password
def set_default_develop_data():
    """
    sets develop data for 
    the implementation for 
    production implementation
    """
    initial_app = (models.Application.
                   objects.get(name='Bookings FGPC DEVELOP'))
    qr_v_credentials = (models.
                        ValidatorCredential.
                        objects.
                        get_or_create(
                            application=initial_app,
                            token='94dd2ea070123000af8effe5faa88577a9824d8f'
                        )[0])
    qr_user = (models.
               User.
               objects.
               get_or_create(
                   username='FPGC qr reader',
                   password=make_password('@12345678')
               )[0])

    qr_validator = (models.
                    QRValidator.
                    objects.
                    get_or_create(
                        user=qr_user,
                        application=initial_app,
                        credentials=qr_v_credentials)[0]
                    )
    
def set_up_qr_default_data():
    """
    sets the inital setup data
    we require in order to get 
    the project running
    :returns: None
    """
    set_default_develop_data()