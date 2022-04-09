from django_restql.mixins import DynamicFieldsMixin
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.company.models import Company
from apps.company.serializers import CompanyReadSerializer
from apps.stock.models import *
from lib.middleware import NoAuditSerializer


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
        fields = ("id", "key", "value",)


class ProductReadSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    company = CompanyReadSerializer()
    brand = BrandSerializer()
    category = CategorySerializer()
    metadata = ProductMetaDataSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "company",
            "brand",
            "category",
            "name",
            "description",
            "sku",
            "purchase_price",
            "selling_price",
            "logo",
            "quantity",
            "metadata",
            "is_available",
            "is_active"
        )


class ProductWriteSerializer(WritableNestedModelSerializer):
    company = PrimaryKeyRelatedField(many=False, required=True, queryset=Company.objects.all())
    brand = PrimaryKeyRelatedField(many=False, required=False, queryset=Brand.objects.all())
    category = PrimaryKeyRelatedField(many=False, required=False, queryset=Category.objects.all())
    metadata = ProductMetaDataSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
