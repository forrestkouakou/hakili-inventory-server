import secrets

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.stock.models import Product, OrderItem
from lib.middleware import generate_string


@receiver(pre_save, sender=Product)
def set_sku(sender, instance, **kwargs):
    if instance.id is None and instance.sku == "":
        instance.sku = secrets.token_hex(5).upper()

@receiver(pre_save, sender=OrderItem)
def set_code(sender, instance, **kwargs):
    if instance.id is None and instance.code == "":
        instance.code = "#{}".format(generate_string(9))


"""
@receiver(pre_save, sender=Product)
def set_product_availability(sender, instance, **kwargs):
    if instance.quantity - instance.orderitem.quantity == 0:
        instance.is_available = False
"""
