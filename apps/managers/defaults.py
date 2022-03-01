from django.core.exceptions import FieldError
from django.db import models

from lib.enums import ACTIVATED


class GlobalQuerySet(models.QuerySet):
    def published(self, status=ACTIVATED):
        """Returns published objects"""
        try:
            return self.filter(status=status)
        except FieldError:
            return self
