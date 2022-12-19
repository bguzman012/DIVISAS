from django.apps import AppConfig


class AppdivsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appdivs'
    
    def ready(self):
        from jobs import updater
        updater.start()
        
