from django.db import models
from django.utils.translation import gettext_lazy as _


class WebActionHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    # user = models.CharField(max_length = 255)
    entity = models.CharField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=255, blank=True, null=True)
    request_id = models.CharField(max_length=255, blank=True, null=True)
    action_name = models.CharField(max_length=255)
    out_state = models.BooleanField(null=True)
    out_msg = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        return

    class Meta:
        db_table = "web_action_history"
        ordering = ["-datetime"]
        verbose_name = _("Web Log")
        verbose_name_plural = _("Web Logs")

    def __str__(self):
        return self.item + " - " + str(self.datetime)
