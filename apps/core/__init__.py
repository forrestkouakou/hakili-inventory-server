import os

from django.conf import settings
from django.contrib.auth.models import Permission


class AppConfig:
    def __init__(self):
        self.django_apps = ["admin", "auth", "authtoken", "contenttypes", "sessions"]

        for app in os.listdir(settings.APPS_DIR):
            if app in self.register_apps():
                pass

    @staticmethod
    def register_apps():
        return [
            "user",
        ]

    @staticmethod
    def register_urls():
        return [
            'apps.user.urls',
        ]

    def app_permissions(self):
        return Permission.objects.exclude(content_type__app_label__in=self.django_apps)


apps_config = AppConfig()
