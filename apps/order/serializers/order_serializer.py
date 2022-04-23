from django_restql.mixins import DynamicFieldsMixin

from apps.order.models import (
    Order,
    OrderItem,
)
from lib.middleware import NoAuditSerializer


class OrderSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(DynamicFieldsMixin, NoAuditSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
