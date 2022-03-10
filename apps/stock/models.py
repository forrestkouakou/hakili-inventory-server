from django.db import models
from django.utils.translation import gettext_lazy as _

from lib.middleware import Monitor


class Brand(Monitor):
    label = models.CharField(_("Brand"), max_length=120)
    summary = models.TextField(_("Summary"))

    class Meta:
        db_table = "brand"