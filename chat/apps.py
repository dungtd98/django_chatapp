from django.apps import AppConfig
from django.db.models.signals import post_save
class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready(self):
        from .signals import publish_event
        from django.contrib.admin.models import LogEntry
        post_save.connect(publish_event, sender=LogEntry)
        return super().ready()
        
        