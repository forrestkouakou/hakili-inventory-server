from django.contrib.auth import get_user_model
from django_restql.mixins import DynamicFieldsMixin

from apps.company.serializers import CompanySerializer
from apps.user.models import UserPermission
from lib.middleware import NoAuditSerializer


class UserPermissionSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = UserPermission
        fields = "__all__"


class UserSerializer(DynamicFieldsMixin, NoAuditSerializer):
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = ("password",)
        extra_kwargs = {
            "username": {"required": False},
            "email": {"required": False}
        }
