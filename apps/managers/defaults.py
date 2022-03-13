from django.core.exceptions import FieldError
from django.db import models


class GlobalQuerySet(models.QuerySet):
    def published(self, status=True):
        """Returns published objects"""
        try:
            return self.filter(status=status)
        except FieldError:
            return self
