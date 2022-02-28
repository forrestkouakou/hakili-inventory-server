from django.db import models
from django.utils.translation import gettext_lazy as _


class WebActionHistory(models.Model):
    action_history_id = models.BigAutoField(primary_key=True)
    """Remove action_history_user"""
    # action_history_user = models.CharField(max_length = 255)
    action_history_table_name = models.CharField(max_length=255, blank=True, null=True)
    action_history_item = models.CharField(max_length=255, blank=True, null=True)
    action_history_request_id = models.CharField(max_length=255, blank=True, null=True)
    action_history_action_name = models.CharField(max_length=255)
    action_history_out_state = models.CharField(max_length=255)
    action_history_out_msg = models.TextField()
    action_history_datetime = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        return

    class Meta:
        db_table = "web_action_history"
        ordering = ["-action_history_datetime"]
        verbose_name = _("Web Log")
        verbose_name_plural = _("Web Logs")

    def __str__(self):
        return self.action_history_item + " - " + str(self.action_history_datetime)
