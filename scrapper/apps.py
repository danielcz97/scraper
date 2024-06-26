from django.apps import AppConfig

class ScrapperConfig(AppConfig):
    name = 'scrapper'

    def ready(self):
        import scrapper.signals
