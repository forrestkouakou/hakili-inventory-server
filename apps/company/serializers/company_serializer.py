from django_countries.serializers import CountryFieldMixin
from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.company.models import (
    CompanyType,
    CompanyPermission,
    CompanyRole,
    Company,
    CompanyDetails,
)


class CompanyTypeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = ("id", "label",)


class CompanyPermissionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CompanyPermission
        fields = (
            'id',
            'name',
            'codename'
        )


class CompanyRoleReadSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    permissions = CompanyPermissionSerializer(many=True)

    class Meta:
        model = CompanyRole
        fields = ("id", "label", "permissions",)


class CompanyRoleWriteSerializer(WritableNestedModelSerializer):
    permissions = PrimaryKeyRelatedField(many=True, required=False, queryset=CompanyPermission.objects.all())

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
            "config"
        )


class CompanyReadSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    company_type = CompanyTypeSerializer()
    company_details = CompanyDetailsSerializer()
    roles = CompanyRoleReadSerializer(many=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "company_type",
            "name",
            "domain",
            "logo",
            "company_details",
            "is_active",
            "roles",
        )


class CompanyWriteSerializer(WritableNestedModelSerializer):
    company_type = PrimaryKeyRelatedField(many=False, required=False, queryset=CompanyType.objects.all())
    company_details = CompanyDetailsSerializer(many=False, required=False)
    roles = PrimaryKeyRelatedField(many=True, required=False, queryset=CompanyRole.objects.all())

    class Meta:
        model = Company
        fields = "__all__"
