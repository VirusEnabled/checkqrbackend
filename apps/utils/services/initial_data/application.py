from apps.application.models import (
    Application,
    ApplicationConfiguration,
    ApplicationUrl,
    ApplicationTag
)

def setup_production_default():
    application_tag = (ApplicationTag.
                       objects.
                       get_or_create(name='bookingfgpc')[0])
    bookings_fgpc = (Application.
                    objects.
                    get_or_create(
                                name='Bookings FGPC',
                                description='Application for making \
                                    reservations at the natural reserve',
                                tag=application_tag
                                )[0])

    bookings_fgpc_config = (ApplicationConfiguration.
                            objects.
                            get_or_create(
                                application=bookings_fgpc,
                                base_url='https://blackbox.puntacana.org/api/',
                                implements_input_search=True
                            )[0])

    bookings_fgpc_confirm_url = (ApplicationUrl.
                                 objects.
                                 get_or_create(
                                    name='confirm_booking_GET',
                                    application=bookings_fgpc,
                                    description='confirms the given booking',
                                    url='confirm_booking/'
                                 ))
    bookings_fgpc_confirm_url = (ApplicationUrl.
                                 objects.
                                 get_or_create(
                                    name='confirm_booking_POST',
                                    application=bookings_fgpc,
                                    description='confirms the given booking',
                                    url='confirm_booking/'
                                 ))

def setup_develop_default():
    application_tag = (ApplicationTag.
                       objects.
                       get_or_create(name='bookingfgpc')[0])
    bookings_dev_fgpc = (Application.
                         objects.
                         get_or_create(
                                name='Bookings FGPC DEVELOP',
                                description='Application for making \
                                    reservations at the natural reserve DEVELOP',
                                tag=application_tag
                                )[0])

    bookings_dev_fgpc_config = (ApplicationConfiguration.
                                objects.
                                get_or_create(
                                    application=bookings_dev_fgpc,
                                    base_url='https://bookingsfgpc-develop.puntacana.com/api/',
                                    implements_input_search=True

                                )[0])

    bookings_dev_fgpc_confirm_url = (ApplicationUrl.
                                     objects.
                                     get_or_create(
                                        name='confirm_booking_GET',
                                        application=bookings_dev_fgpc,
                                        description='confirms the given booking',
                                        url='confirm_booking/'
                                    ))
    bookings_dev_fgpc_confirm_url = (ApplicationUrl.
                                     objects.
                                     get_or_create(
                                        name='confirm_booking_POST',
                                        application=bookings_dev_fgpc,
                                        description='confirms the given booking',
                                        url='confirm_booking/'
                                    ))


def set_application_default_data(env='dev'):
    """
    sets the default data required
    for the project to startup
    """
    if env =='prod':
        setup_production_default()

    else:
        setup_develop_default()
