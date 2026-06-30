from django.apps import AppConfig


class LdeaConfig(AppConfig):
    name = 'ldea'

class YourAppConfig(AppConfig):
    name = "ldea"

    def ready(self):
        import ldea.signals