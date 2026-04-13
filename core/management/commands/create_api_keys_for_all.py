from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from core.models.api_keys import UserAPIKey


class Command(BaseCommand):
    help = 'Create the Initial Admin User, if necessary'

    def handle(self, *args, **options):
        User = get_user_model()

        try:
            users_without_api_keys = User.objects.filter(
                api_keys__isnull=True
            ).all()
            did_create_api_key = False
            for user in users_without_api_keys:
                api_key, key = UserAPIKey.objects.create_key(
                    user=user,
                    name=user.username
                )
                # This is so dumb...
                api_key.key = key
                api_key.save()
                did_create_api_key = True
            if did_create_api_key:
                self.stdout.write("Api Keys Created")
            else:
                self.stdout.write("All Users already have Api Key")
        except Exception as e:
            raise CommandError(str(e))
