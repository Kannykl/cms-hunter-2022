from django.core.management.base import BaseCommand
import config.settings as settings
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = settings.ADMIN
        password = 'admin'
        print(f'Creating super user account for {admin}')
        admin = User.objects.create_superuser(username=admin, password=password)
        admin.is_active = True
        admin.is_admin = True
        admin.save()
