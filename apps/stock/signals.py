from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.stock.models import Product


@receiver(pre_save)
@receiver(pre_save, sender=Product)
def update_code(sender, instance, **kwargs):
    if instance.id is None:
        pass
