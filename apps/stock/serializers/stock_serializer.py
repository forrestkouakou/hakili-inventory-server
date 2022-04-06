from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from apps.company.models import Company
from apps.company.serializers import CompanyReadSerializer
from apps.stock.models import *


class BrandSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "company", "label", "description", "is_active",)


class CategorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "company", "label", "description", "is_active",)


class ProductMetaDataSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductMetaData
        fields = ("key", "value",)


class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    company = CompanyReadSerializer()
    brand = BrandSerializer()
    category = CategorySerializer()
    meta_data = ProductMetaDataSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
