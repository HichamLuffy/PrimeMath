from django.apps import AppConfig


class PrmathConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Prmath'

    def ready(self):
        import Prmath.signals
