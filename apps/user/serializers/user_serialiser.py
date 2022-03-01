from django.contrib.auth import get_user_model
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

# from lib.middleware import DynamicSerializer
from apps.company.serializers import CompanySerializer
from apps.user.models import UserPermission


class UserPermissionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = "__all__"


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = ("password",)
        extra_kwargs = {
            "username": {"required": False},
            "email": {"required": False}
        }
