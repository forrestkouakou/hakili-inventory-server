from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from apps.stock.models import *


class BrandSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "label", "is_active",)


class CategorySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "label", "is_active",)


class ProductMetaDataSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("key", "value",)


class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
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
