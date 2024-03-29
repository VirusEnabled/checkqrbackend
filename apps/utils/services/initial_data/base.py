from .application import set_application_default_data
from .qr import set_up_qr_default_data

def set_default_data(env=None):
    """
    sets the default data
    for the whole project
    to start it up
    :returns: None
    """
    set_application_default_data(env=env)
    set_up_qr_default_data(env=env)