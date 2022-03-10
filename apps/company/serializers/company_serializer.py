from django_countries.serializers import CountryFieldMixin
from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.company.models import *
from apps.user.models import UserPermission
from apps.user.serializers import UserPermissionSerializer


class CompanyTypeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = ("id", "label",)


class CompanyRoleReadSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    permissions = UserPermissionSerializer(many=True)

    class Meta:
        model = CompanyRole
        fields = ("id", "label", "permissions",)


class CompanyRoleWriteSerializer(serializers.ModelSerializer):
    permissions = PrimaryKeyRelatedField(many=True, required=False, queryset=UserPermission.objects.all())

    class Meta:
        model = CompanyRole
        fields = "__all__"


class CompanyDetailsSerializer(CountryFieldMixin, DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = (
            "cc_name",
            "trading_name",
            "currency",
            "email",
            "country",
            "phone",
            "fax",
            "post_code",
        )


class CompanyReadSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    company_type = CompanyTypeSerializer()
    company_details = CompanyDetailsSerializer()
    roles = CompanyRoleReadSerializer(many=True)

    class Meta:
        model = Company
        fields = (
            "company_type",
            "name",
            "domain",
            "logo",
            "status",
            "company_details",
            "roles",
        )


class CompanyWriteSerializer(DynamicFieldsMixin, WritableNestedModelSerializer):
    company_type = PrimaryKeyRelatedField(many=False, required=False, queryset=CompanyType.objects.all())
    company_details = CompanyDetailsSerializer(many=False, required=False)
    roles = PrimaryKeyRelatedField(many=True, required=False, queryset=CompanyRole.objects.all())

    class Meta:
        model = Company
        fields = "__all__"
