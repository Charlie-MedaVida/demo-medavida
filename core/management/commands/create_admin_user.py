import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError




class Command(BaseCommand):
    help = 'Create the Initial Admin User, if necessary'

    def handle(self, *args, **options):
        User = get_user_model()

        try:
            ADMIN_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            admin_exists = User.objects.filter(username=ADMIN_USERNAME).exists()
            if admin_exists:
                self.stdout.write(f"Admin User exists...")
                self.stdout.write(f"Skipping create_admin_users Command")
                return
            self.stdout.write(f"Creating Admin User...")
            ADMIN_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            ADMIN_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            self.stdout.write(f"Admin User Created")
        except Exception as e:
            raise CommandError(str(e))
