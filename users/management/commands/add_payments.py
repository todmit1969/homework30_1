from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'payments.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data form fixture'))