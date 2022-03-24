from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from lib.enums import PAYMENT_TYPE
from lib.middleware import Monitor, Hider, upload_path


class Brand(Monitor):
    label = models.CharField(_("Brand"), max_length=120)
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        app_label = "stock"
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ["label"]

    def __str__(self):
        return self.label


class Category(Monitor):
    label = models.CharField(_("Label"), max_length=120)
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        app_label = "stock"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["label"]

    def __str__(self):
        return self.label


class Product(Monitor):
    company = models.ForeignKey("company.Company", models.CASCADE, verbose_name=_("Company"))
    brand = models.ForeignKey(Brand, models.SET_NULL, blank=True, null=True, verbose_name=_("Brand"))
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True, verbose_name=_("Category"))
    name = models.CharField(_("Name"), max_length=255)
    summary = models.TextField(_("Summary"), blank=True)
    code = models.CharField(_("Code"), max_length=10, blank=True, default="")
    price = models.DecimalField(_("Price"), max_digits=15, decimal_places=3, default=0)
    logo = VersatileImageField(upload_to=upload_path, blank=True, null=True)
    quantity = models.PositiveIntegerField(_("Quantity"), blank=True, null=True)
    # rate = models.FloatField(_("Rate"), blank=True, null=True)
    meta_data = models.ManyToManyField("ProductMetaData", related_name="metadata")
    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        app_label = "stock"
        verbose_name = _("Product")
        verbose_name_plural = _("Product")
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProductMetaData(Monitor):
    key = models.CharField(_("Key"), max_length=60)
    value = models.CharField(_("Value"), max_length=120)

    class Meta:
        app_label = "stock"
        verbose_name = _("Product meta")
        verbose_name_plural = _("Product meta")


class Order(Monitor):
    sub_total = models.DecimalField(_("Sub total"), max_digits=15, decimal_places=3, default=0)
    vat = models.DecimalField(_("Vat"), max_digits=5, decimal_places=2, default=0)
    total_amount = models.DecimalField(_("Total amount"), max_digits=15, decimal_places=3, default=0)
    discount = models.DecimalField(_("Discount"), max_digits=15, decimal_places=3, default=0)
    grand_total = models.DecimalField(_("Grand total"), max_digits=15, decimal_places=3, default=0)
    paid = models.DecimalField(_("Paid"), max_digits=15, decimal_places=3, default=0)
    due = models.DecimalField(_("Due"), max_digits=15, decimal_places=3, default=0)
    payment_type = models.CharField(_("Payment type"), choices=PAYMENT_TYPE, max_length=20, blank=True, default="")
    payment_status = models.IntegerField()
    status = models.IntegerField()

    updated_at = Hider()

    class Meta:
        app_label = "stock"
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(Monitor):
    order = models.ForeignKey(Order, models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(Product, models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(_("Quantity"), validators=[MinValueValidator(1)])
    rate = models.DecimalField(_("Rate"), max_digits=15, decimal_places=3, default=0)
    total = models.DecimalField(_("Total"), max_digits=15, decimal_places=3, default=0)
    status = models.IntegerField()

    class Meta:
        app_label = "stock"
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
