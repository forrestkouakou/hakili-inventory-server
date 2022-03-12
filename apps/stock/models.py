from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from lib.middleware import Monitor, Hider, upload_path


class Brand(Monitor):
    label = models.CharField(_("Brand"), max_length=120)
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ["label"]

    def __str__(self):
        return self.label


class Category(Monitor):
    label = models.CharField(_("Label"), max_length=120)
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["label"]

    def __str__(self):
        return self.label


class Product(Monitor):
    brand = models.ForeignKey(Brand, models.SET_NULL, blank=True, null=True, verbose_name=_("Brand"))
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True, verbose_name=_("Category"))
    name = models.CharField(_("Name"), max_length=255)
    summary = models.TextField(_("Summary"), blank=True)
    code = models.CharField(_("Code"), max_length=10, blank=True, default="")
    price = models.DecimalField(_("Price"), max_digits=15, decimal_places=0, default=0)
    logo = VersatileImageField(upload_to=upload_path, blank=True, null=True)
    quantity = models.IntegerField(_("Quantity"), blank=True, null=True)
    rate = models.FloatField(_("Rate"), blank=True, null=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Product")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(Monitor):
    sub_total = models.FloatField(max_length=100)
    vat = models.FloatField(max_length=100)
    total_amount = models.FloatField(max_length=100)
    discount = models.FloatField(max_length=100)
    grand_total = models.FloatField(max_length=100)
    paid = models.FloatField(max_length=100)
    due = models.FloatField(max_length=100)
    payment_type = models.CharField(max_length=100)
    payment_status = models.IntegerField()
    status = models.IntegerField()

    updated_at = Hider()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(Monitor):
    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    quantity = models.IntegerField()
    rate = models.FloatField(max_length=100)
    total = models.FloatField(max_length=100)
    status = models.IntegerField()

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
