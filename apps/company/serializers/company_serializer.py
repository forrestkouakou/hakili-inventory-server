from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.company.models import *
from lib.middleware import DynamicSerializer


class CompanyTypeSerializer(DynamicSerializer):
    class Meta:
        model = CompanyType
        fields = "__all__"


class CompanySerializer(DynamicSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyDetailsSerializer(CountryFieldMixin, DynamicSerializer):
    # country = CountryField(country_dict=True)

    class Meta:
        model = CompanyDetails
        fields = "__all__"
