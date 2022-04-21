from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from lib.enums import STATUS_CHOICES
from lib.middleware import Monitor, upload_path


class Brand(Monitor):
    """
    The Brand Table to store the brand data
    """
    company = models.ForeignKey('company.Company', models.CASCADE, verbose_name=_('Company'))
    label = models.CharField(_('Brand'), max_length=120)
    description = models.TextField(_('Description'), blank=True, default='')
    is_active = models.BooleanField(_('Is active'), choices=STATUS_CHOICES, default=True)

    class Meta:
        app_label = 'product'
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['label']
        unique_together = ('company', 'label',)

    def __str__(self):
        return self.label


class Category(Monitor):
    """
    The Category Table to store the product categories.
    """
    company = models.ForeignKey('company.Company', models.CASCADE, verbose_name=_('Company'))
    label = models.CharField(_('Label'), max_length=120)
    description = models.TextField(_('Description'), blank=True, default='')
    is_active = models.BooleanField(_('Is active'), choices=STATUS_CHOICES, default=True)

    # slug = models.CharField(_('Slug'), max_length=100)

    class Meta:
        app_label = 'product'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['label']
        unique_together = ('company', 'label',)

    def __str__(self):
        return self.label


class Product(Monitor):
    """
    The Product Table to store the product data.
    """
    company = models.ForeignKey('company.Company', models.CASCADE, verbose_name=_('Company'))
    brand = models.ForeignKey(Brand, models.SET_NULL, blank=True, null=True, verbose_name=_('Brand'))
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True, verbose_name=_('Category'))
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    sku = models.CharField(_('SKU'), max_length=15, unique=True, default='', editable=False)
    logo = VersatileImageField(_('Logo'), upload_to=upload_path, blank=True, null=True)
    # slug = models.SlugField(_('Slug'), unique=True)
    purchase_price = models.DecimalField(_('Unit purchase price'), max_digits=15, decimal_places=3, default=0)
    selling_price = models.DecimalField(_('Unit selling price'), max_digits=15, decimal_places=3, default=0)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    max_alert_threshold = models.PositiveIntegerField(_('Max alert threshold'), blank=True, null=True)
    min_alert_threshold = models.PositiveIntegerField(_('Min alert threshold'), blank=True, null=True)
    metadata = models.ManyToManyField('ProductMetaData', related_name='products', blank=True)
    is_available = models.BooleanField(_('Is available'), default=True)
    is_active = models.BooleanField(_('Is active'), choices=STATUS_CHOICES, default=True)

    class Meta:
        app_label = 'product'
        verbose_name = _('Product')
        verbose_name_plural = _('Product')
        ordering = ['name']
        unique_together = ('company', 'name',)

    def __str__(self):
        return '{}: {}'.format(self.company, self.name)


class ProductMetaData(Monitor):
    """
    The Product Meta Table can be used to store additional information about products including the product banner URL etc.
    """
    key = models.CharField(_('Key'), max_length=60)
    value = models.CharField(_('Value'), max_length=120)

    class Meta:
        app_label = 'product'
        verbose_name = _('Product meta')
        verbose_name_plural = _('Product meta')
