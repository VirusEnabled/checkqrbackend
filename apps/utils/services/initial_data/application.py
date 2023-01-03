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
    
    sscc_application_tag = (ApplicationTag.
                       objects.
                       get_or_create(name='sscc')[0])
    sscc = (Application.
            objects.
            get_or_create(
                name='SSCC_PRODUCTION',
                description='sistema de carnetizacion, \
                    esta integracion es para probar con los marbetes vehiculares',
                tag=sscc_application_tag
                )[0])

    sscc_config = (ApplicationConfiguration.
                    objects.
                    get_or_create(
                        application=sscc,
                        base_url='https://sscc.puntacana.com',
                        implements_input_search=True

                    )[0])

    sscc_confirm_url = (ApplicationUrl.
                        objects.
                        get_or_create(
                        name='check_marbete_GET',
                        application=sscc,
                        description='carga la informacion del marbete',
                        url='/marbete/verifica_marbete/'
                    ))
    sscc_confirm_url = (ApplicationUrl.
                        objects.
                        get_or_create(
                        name='confirm_booking_POST',
                        application=sscc,
                        description='envia un post al url en base a las politicas utilizadas',
                        url='/marbete/verifica_marbete/'
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

    sscc_application_tag = (ApplicationTag.
                       objects.
                       get_or_create(name='sscc')[0])
    sscc_dev = (Application.
                         objects.
                         get_or_create(
                                name='SSCC_DEVELOP',
                                description='sistema de carnetizacion, \
                                    esta integracion es para probar con los marbetes vehiculares',
                                tag=sscc_application_tag
                                )[0])

    sscc_dev_config = (ApplicationConfiguration.
                                objects.
                                get_or_create(
                                    application=sscc_dev,
                                    base_url='https://sscc-develop.puntacana.com',
                                    implements_input_search=True

                                )[0])

    sscc_dev_confirm_url = (ApplicationUrl.
                                     objects.
                                     get_or_create(
                                        name='check_marbete_GET',
                                        application=sscc_dev,
                                        description='carga la informacion del marbete',
                                        url='/marbete/verifica_marbete/'
                                    ))
    sscc_dev_confirm_url = (ApplicationUrl.
                                     objects.
                                     get_or_create(
                                        name='confirm_booking_POST',
                                        application=sscc_dev,
                                        description='envia un post al url en base a las politicas utilizadas',
                                        url='/marbete/verifica_marbete/'
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
