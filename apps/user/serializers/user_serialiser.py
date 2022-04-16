from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# from apps.company.serializers import CompanySerializer
# from apps.company.serializers import CompanyReadSerializer
from apps.core.models import Installation
from apps.user.models import UserPermission
from lib.middleware import NoAuditSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2', 'company')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": gettext_lazy("Password fields didn't match.")})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserPermissionSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = UserPermission
        fields = "__all__"


class UserSerializer(DynamicFieldsMixin, NoAuditSerializer):
    # company = CompanySerializer(many=False, read_only=True)

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = ("password",)
        extra_kwargs = {
            "username": {"required": False, "write_only": True},
            "email": {"required": False}
        }


class UserReadSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    # company = CompanyReadSerializer()
    # permissions = UserPermissionSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "company",
            "first_name",
            "last_name",
            "email",
            "username",
            "avatar",
            "phone",
            "is_active",
            "is_admin",
            "date_joined",
            "email_confirmed",
            "permissions",
        )


"""
class UserWriteSerializer(WritableNestedModelSerializer):
    company = CompanyReadSerializer(many=False, required=False)
    # permissions = PrimaryKeyRelatedField(many=True, required=False, queryset=UserPermission.objects.all())

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = ("password",)
        extra_kwargs = {
            "username": {"required": False, "write_only": True},
            "email": {"required": False}
        }
"""


class InstallationSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = Installation
        fields = "__all__"
