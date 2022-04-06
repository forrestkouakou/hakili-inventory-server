from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from apps.user.models import User
from apps.user.token import account_activation_token
from hakili.settings import env
from lib.middleware import notifier


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    """Send email to created user"""
    if created:
        if instance.is_superuser is False:
            notify_data = {
                "action": "creation",
                "e_subject": "{} - {}".format(env("APP_NAME"), _("User Creation")),
                "e_receiver": instance.email,
                "e_context": {
                    "api_version": "v1",
                    "user": instance,
                    "uid": urlsafe_base64_encode(force_bytes(instance.pk)),
                    "token": account_activation_token.make_token(instance),
                    "domain": Site.objects.get_current().domain,
                }
            }
            notifier(**notify_data)

            instance.save()
