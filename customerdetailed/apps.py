# A - Imports
from django.apps import AppConfig

# B - App Configuration
class CustomerdetailedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customerdetailed'

    # C - Signal Registration
    def ready(self):
        import customerdetailed.signals


