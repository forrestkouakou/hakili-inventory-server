import secrets

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.product.models import Product
from lib.middleware import generate_string


@receiver(pre_save, sender=Product)
def set_sku(sender, instance, **kwargs):
    if instance.id is None and instance.sku == "":
        instance.sku = "{}{}".format(secrets.token_hex(5).upper(), generate_string(5, 'pin'))


@receiver(pre_save, sender=Product)
def set_product_availability(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.is_available = False
        instance.save()
