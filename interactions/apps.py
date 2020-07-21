from django.apps import AppConfig


class InteractionsConfig(AppConfig):
    name = 'interactions'

    def ready(self):
        import interactions.signals
