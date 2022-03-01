# from lib.middleware import DynamicSerializer
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from apps.company.models import *
from lib.middleware import NoAuditSerializer


class CompanyTypeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = "__all__"


class CompanyRoleSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = CompanyRole
        fields = "__all__"


class CompanyDetailsSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = CompanyDetails
        fields = "__all__"


class CompanySerializer(DynamicFieldsMixin, NoAuditSerializer):
    roles = CompanyRoleSerializer(many=True, read_only=True)
    company_details = CompanyDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
