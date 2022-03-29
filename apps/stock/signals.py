import secrets

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.stock.models import Product


@receiver(pre_save, sender=Product)
def set_sku(sender, instance, **kwargs):
    if instance.id is None and instance.sku == "":
        instance.sku = secrets.token_hex(5).upper()


@receiver(pre_save, sender=Product)
def set_product_availability(sender, instance, **kwargs):
    if instance.quantity - instance.orderitem.quantity == 0:
        instance.is_available = False
