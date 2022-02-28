from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from versatileimagefield.fields import VersatileImageField

from lib.enums import STATUS_CHOICES, ACTIVATED
from lib.middleware import Monitor, upload_path


class CompanyType(Monitor):
    label = models.CharField(_("Company type"), max_length=45, unique=True)

    class Meta:
        db_table = "company_type"
        verbose_name = _("Company type")
        verbose_name_plural = _("Company types")
        ordering = ["label"]

    def __str__(self):
        return self.label


class Company(Monitor):
    company_type = models.ForeignKey(CompanyType, models.DO_NOTHING, blank=True, null=True, verbose_name=_("Company type"))
    name = models.CharField(_("Name"), max_length=120, unique=True)
    domain = models.CharField(_("Domain"), max_length=120, blank=True)
    logo = VersatileImageField(upload_to=upload_path, blank=True, null=True)
    # is_active = models.BooleanField(default=True)
    status = models.BooleanField(_("Status"), choices=STATUS_CHOICES, default=ACTIVATED, null=True)

    class Meta:
        db_table = "company"
        verbose_name = _("Company")
        verbose_name_plural = _("Company")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from lib.middleware import py_slugify
        domain = py_slugify(self.name).upper()
        if self.domain != domain:
            self.domain = domain
        super(Company, self).save(*args, **kwargs)


class CompanyDetails(Monitor):
    company = models.OneToOneField(Company, models.CASCADE, related_name="company_details", verbose_name=_("Company"))
    cc_name = models.CharField(_("Trade Register"), max_length=50, default="")
    trading_name = models.CharField(_("name"), max_length=120, blank=True, default="")
    currency = models.CharField(_("Currency"), max_length=3, default="")
    email = models.CharField(_("Email"), max_length=120, default="")
    country = CountryField(_("Country"), blank=True, default="")
    phone = models.CharField(_("Phone number"), max_length=60, blank=True, default="")
    fax = models.CharField(_("Phone number"), max_length=60, blank=True, default="")
    post_code = models.CharField(_("Post code"), max_length=60, blank=True, default="")

    class Meta:
        db_table = "company_details"
        verbose_name = _("Company Details")
        verbose_name_plural = _("Company Details")
        ordering = ["company"]


class CompanyMembership(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE)
    role = models.ForeignKey("user.UserRole", on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "company_membership"
        verbose_name = _("Company membership")
        verbose_name_plural = _("Company memberships")
        unique_together = ('user', 'company',)
        ordering = ["company"]
