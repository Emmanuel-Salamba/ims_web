from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser automatically if none exists'

    def handle(self, *args, **options):
        email = os.environ.get('ADMIN_EMAIL', 'admin@ims-malawi.org')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
        username = os.environ.get('ADMIN_USERNAME', 'admin')

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists, skipping creation.'))
