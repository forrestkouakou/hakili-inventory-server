import functools
import os

from django.conf import settings
from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.response import Response

from apps.company.models import Company


class AppConfig:
    READ_METHODS = ["GET"]
    WRITE_METHODS = ["POST", "PUT", "PATCH"]

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

    def get_method_type(self, method_type="read|write"):
        if method_type is not None:
            pass

    @staticmethod
    def company_404_handler(func):
        @functools.wraps(func)
        def wrapper(self):
            try:
                company_id = self.kwargs.get("company_pk", 1)
                Company.objects.company_list().get(id=company_id)
                func(self)
                return func(self)
            except Company.DoesNotExist:
                return {"self": "jk"}

        return wrapper


apps_config = AppConfig()
