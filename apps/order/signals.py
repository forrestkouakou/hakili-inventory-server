from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.order.models import OrderItem
from lib.middleware import generate_string


@receiver(pre_save, sender=OrderItem)
def set_code(sender, instance, **kwargs):
    if instance.id is None and instance.code == "":
        instance.code = "#{}".format(generate_string(9))
