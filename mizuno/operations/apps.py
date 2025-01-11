from django.apps import AppConfig


class OperationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'operations'

    def ready(self):
        import operations.signals  # 導入 signals.py 中的訊號處理函數