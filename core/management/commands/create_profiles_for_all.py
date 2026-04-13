from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from core.models import Profile


class Command(BaseCommand):
    help = 'Create the Initial Admin User, if necessary'

    def handle(self, *args, **options):
        User = get_user_model()

        try:
            users_without_api_keys = User.objects.filter(
                profile__isnull=True
            ).all()
            did_create_profile = False
            for user in users_without_api_keys:
                Profile.objects.create(user=user)
                did_create_profile = True
            if did_create_profile:
                self.stdout.write("User Profiles Created")
            else:
                self.stdout.write("All Users already have Profiles")
        except Exception as e:
            raise CommandError(str(e))
