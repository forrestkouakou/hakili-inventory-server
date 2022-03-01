from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
from apps.company.models import Company
from apps.managers.defaults import GlobalQuerySet


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError(_('User must have an email address'))
        if not password:
            raise ValueError(_('User must have Password'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, company=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        # Try to get the fake company
        try:
            company = Company.objects.get(name="...")
        except Company.DoesNotExist:
            if not company:
                company = Company(
                    name="...",
                )
                company.save()

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(email, password=password, company=company, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserQuerySet(GlobalQuerySet):
    def reserved_user_list(self):
        """Returns reserved user_list"""
        return self.filter(id__in=[1])

    def user_list(self):
        """Returns all available user list"""
        return self.exclude(id__in=[1])
