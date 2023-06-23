from django.core.management.base import BaseCommand
from apps.utils.services.initial_data import base


class Command(BaseCommand):
    help = 'Sets all of the default data required to start the system.'

    def add_arguments(self, parser) -> None:
        parser.add_argument('env', help='environment to run the data based the configuration', default='dev')
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        env = options['env']
        base.set_default_data(env=env)
        (self.stdout.
         write(self.style.
               SUCCESS('Successfully created default records.')))
