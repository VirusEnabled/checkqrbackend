from django.core.management.base import BaseCommand
from apps.utils.services.initial_data import base


class Command(BaseCommand):
    help = 'Sets all of the default data required to start the system.'

    def handle(self, *args, **options):
        base.set_default_data()
        (self.stdout.
         write(self.style.
               SUCCESS('Successfully created default records.')))
