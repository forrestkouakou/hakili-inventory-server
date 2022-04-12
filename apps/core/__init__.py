import os

from django.conf import settings
# from apps.company.models import Company
# from django.contrib.auth.models import Permission
from django.db import IntegrityError

from lib.config import django_logger


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

    # def app_permissions(self):
    # return Permission.objects.exclude(content_type__app_label__in=self.django_apps)

    def get_method_type(self, method_type="read|write"):
        if method_type is not None:
            pass

    """
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
    """

    @staticmethod
    def save_handler(klass_object):
        try:
            klass_object.save()
            return klass_object
        except (IntegrityError, ValueError, KeyError) as e:
            django_logger.error("{}".format(e))
            return False


apps_config = AppConfig()
