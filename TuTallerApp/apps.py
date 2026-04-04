from django.apps import AppConfig
from django.apps import AppConfig

class TuTallerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TuTallerApp'
    verbose_name = "Sistema de Gestión TuTaller"
    
    
    
    



class TuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TuTallerApp'

    def ready(self):
        import TuTallerApp.signals   # 👈 🔥 ESTO ES OBLIGATORIO