from django.apps import AppConfig


class CRMConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'

    def ready(self):
        import crm.signals  # 引入信號
