import os

from django.conf import settings
from django.contrib.auth.models import Permission
from rest_framework import serializers


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


class DynamicSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        # get the original representation
        ret = super(DynamicSerializer, self).to_representation(obj)

        # remove audit fields
        ret.pop('created_at')
        ret.pop('updated_at')
        ret.pop('created_by')
        ret.pop('updated_by')

        # here write the logic to check whether `elements` field is to be removed
        # pop 'elements' from 'ret' if condition is True

        # return the modified representation
        return ret

apps_config = AppConfig()
