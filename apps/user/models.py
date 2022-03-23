from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from apps.managers import UserManager, UserQuerySet
from lib.middleware import Monitor, upload_path


class User(AbstractBaseUser, PermissionsMixin, Monitor):
    company = models.ForeignKey("company.Company", models.CASCADE, verbose_name=_("Company"))
    first_name = models.CharField(_("First name"), max_length=60, blank=True, default="")
    last_name = models.CharField(_("Last name"), max_length=120, blank=True, default="")
    email = models.EmailField(_("Email address"), max_length=225, unique=True)
    username = models.CharField(_("Username"), max_length=30)
    avatar = VersatileImageField(_("Avatar"), upload_to=upload_path, blank=True, null=True)
    phone = models.CharField(_("Phone number"), max_length=15, blank=True, default="")
    is_active = models.BooleanField(_("Is active"), default=False)
    is_admin = models.BooleanField(_("Is admin"), default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    email_confirmed = models.BooleanField(_("Email confirmed"), default=False)

    objects = UserManager()
    people = UserQuerySet.as_manager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "user"
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('-created_at', '-updated_at',)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        username = self.email.split('@')[0]
        if not self.username:
            self.username = username
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        if self.first_name:
            return "{} {}".format(self.last_name, self.first_name)
        return self.email.split('@')[0]

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = "user"
        db_table = 'user_permission'
        verbose_name = _("User permission")
        verbose_name_plural = _("Users permissions")
        ordering = ['name']

    def __str__(self):
        return self.name
