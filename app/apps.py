from django.apps import AppConfig


class HarmonixAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    
    def ready(self):
        print("⚡ AppConfig ready - signals imported")
        import app.signals  # noqa: F401  # Ensure signals are imported when the app is ready
