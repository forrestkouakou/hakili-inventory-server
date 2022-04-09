import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Installation(models.Model):
    installation_id = models.UUIDField(_("Installation ID"), default=uuid.uuid4, editable=False)
    fcm_token = models.TextField(_("FCM token"), blank=True, default="")
    device_name = models.CharField(_("Device name"), max_length=60, blank=True, default="")
    device_model = models.CharField(_("Device model"), max_length=60, blank=True, default="")
    device_version = models.CharField(_("Device version"), max_length=60, blank=True, default="")
    country_location = models.CharField(_("Country location"), max_length=60, blank=True, default="")
    user_id = models.CharField(_("User ID"), max_length=60, blank=True, default="")
    datetime = models.DateTimeField(_("Datetime"), auto_now_add=True, editable=False)

    def __str__(self):
        return '{} - {}'.format(self.installation_id, self.datetime)

class WebActionHistory(models.Model):
    # user = models.CharField(max_length = 255)
    entity = models.CharField(_("Entity"), max_length=120, blank=True, default="")
    item = models.CharField(_("Item"), max_length=255, blank=True, default="")
    request_id = models.UUIDField(_("Request ID"), default=uuid.uuid4, max_length=255, blank=True, null=True)
    action_name = models.CharField(_("Action name"), max_length=255)
    out_state = models.BooleanField(_("Out state"), null=True)
    out_msg = models.TextField(_("Out msg"))
    datetime = models.DateTimeField(_("Datetime"), auto_now_add=True)

    def delete(self, *args, **kwargs):
        return

    class Meta:
        managed = False
        db_table = "web_action_history"
        ordering = ["-datetime"]
        verbose_name = _("Web Log")
        verbose_name_plural = _("Web Logs")

    def __str__(self):
        return self.item + " - " + str(self.datetime)
