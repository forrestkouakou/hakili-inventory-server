from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from apps.core import DynamicSerializer
from apps.user.models import UserRole


class GroupSerializer(DynamicSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(DynamicSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class UserSerializer(DynamicSerializer):
    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = ("password",)
        extra_kwargs = {
            "username": {"required": False},
            "email": {"required": False}
        }


class UserRoleSerializer(DynamicSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"
