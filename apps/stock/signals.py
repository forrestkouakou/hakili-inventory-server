import secrets

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.stock.models import Product, OrderItem
from lib.middleware import generate_string


@receiver(pre_save, sender=Product)
def set_sku(sender, instance, **kwargs):
    if instance.id is None and instance.sku == "":
        instance.sku = "{}{}".format(secrets.token_hex(5).upper(), generate_string(5, 'pin'))


@receiver(post_save, sender=Product)
def set_order_sub_total(sender, instance, **kwargs):
    if instance.id:
        instance.code = "#{}".format(generate_string(9))


@receiver(pre_save, sender=OrderItem)
def set_code(sender, instance, **kwargs):
    if instance.id is None and instance.code == "":
        instance.code = "#{}".format(generate_string(9))


@receiver(pre_save, sender=OrderItem)
def set_total_amount(sender, instance, **kwargs):
    if instance.id is None and instance.code == "":
        instance.code = "#{}".format(generate_string(9))

@receiver(post_save, sender=OrderItem)
def write_transaction(sender, instance, **kwargs):
    if instance.id:
        pass

"""
@receiver(pre_save, sender=Product)
def set_product_availability(sender, instance, **kwargs):
    if instance.quantity - instance.orderitem.quantity == 0:
        instance.is_available = False
"""
