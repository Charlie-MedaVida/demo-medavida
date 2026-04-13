from django.apps import AppConfig


class VidaVerifiedConfig(AppConfig):
    name = 'vida_verified'

    def ready(self):
        import vida_verified.signal_handlers  # noqa: F401
