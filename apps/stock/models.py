from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from lib.enums import PAYMENT_TYPE, TNX_MODE, TNX_STATUS, ORDER_STATUS, TNX_TYPE, STATUS_CHOICES
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
        app_label = 'stock'
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
        app_label = 'stock'
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
        app_label = 'stock'
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
        app_label = 'stock'
        verbose_name = _('Product meta')
        verbose_name_plural = _('Product meta')


class Order(Monitor):
    """
    The Order Table is used to manage the inventory orders.
    The order can be associated with either Supplier or the Customer.
    """
    company = models.ForeignKey(
        'company.Company',
        models.CASCADE,
        verbose_name=_('Company'),
        help_text='The company the order is related to'
    )
    sub_total = models.DecimalField(
        _('Sub total'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The total price of the Order Items.'
    )
    tax = models.DecimalField(
        _('Tax'),
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='The tax on the Order Items.'
    )
    shipping = models.DecimalField(
        _('Shipping'),
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='The shipping charges of the Order Items.'
    )
    total_amount = models.DecimalField(
        _('Total amount'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The total price of the Order including tax and shipping. It excludes the items discount.'
    )
    discount = models.DecimalField(
        _('Discount'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The total discount of the Order based on the promo code or store discount.'
    )
    grand_total = models.DecimalField(
        _('Grand total'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The grand total of the order to be paid by the buyer.'
    )
    paid = models.DecimalField(
        _('Paid'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The amount already paid on the total.'
    )
    due = models.DecimalField(
        _('Due'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The due to be paid.'
    )
    payment_type = models.CharField(
        _('Payment type'),
        choices=PAYMENT_TYPE,
        max_length=20,
        blank=True,
        default='',
        help_text='The payment type.'
    )
    order_status = models.CharField(
        _('Order status'),
        choices=ORDER_STATUS,
        max_length=20,
        blank=True,
        default='',
        help_text='The status of the order can be New, Checkout, Paid, Failed, Shipped, Delivered, Returned, and Complete.'
    )

    class Meta:
        app_label = 'stock'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(Monitor):
    """
    The Order Item Table is used to manage the order items purchased by the customers.
    """
    code = models.CharField(
        _('Code'),
        max_length=10,
        unique=True,
        default='',
        editable=False,
        help_text='The code of this order, a unique code that will be displayed to the user.'
    )
    order = models.ForeignKey(
        'Order',
        models.CASCADE,
        verbose_name=_('Order'),
        help_text='The order id to identify the order associated with the ordered item.'
    )
    product = models.ForeignKey(
        'Product',
        models.CASCADE,
        verbose_name=_('Product'),
        help_text='The product id to identify the product associated with the ordered item.'
    )
    price = models.DecimalField(
        _('Price'),
        max_digits=15,
        decimal_places=3,
        default=None,
        help_text='The price of the product while purchasing it.'
    )
    discount = models.DecimalField(
        _('Discount'),
        max_digits=15,
        decimal_places=3,
        default=0,
        help_text='The discount of the product while purchasing it.'
    )
    quantity = models.PositiveIntegerField(
        _('Quantity'),
        validators=[MinValueValidator(1)],
        help_text='The quantity of the product selected by the user.'
    )
    summary = models.CharField(
        _('Summary'),
        max_length=225,
        blank=True,
        default='',
        help_text='The summary to mention the key highlights.'
    )

    class Meta:
        app_label = 'stock'
        verbose_name = _('Item')
        verbose_name_plural = _('Items')


class Transaction(Monitor):
    """
    We also need a transaction table to track the order payments made by the buyer and for bookkeeping.
    We can also use the same table to record the partial or full refund of the order.
    """
    user = models.ForeignKey(
        'user.User',
        models.DO_NOTHING,
        blank=True,
        null=True,
        default=True,
        help_text='The user id to identify the user associated with the transaction.',
    )
    order = models.ForeignKey(
        'Order',
        models.DO_NOTHING,
        help_text='The order id to identify the order associated with the transaction.'
    )
    code = models.CharField(
        _('Payment ID'),
        max_length=100,
        blank=True,
        default='',
        help_text='The payment id provided by the payment gateway.'
    )
    type = models.CharField(
        _('Transaction type'),
        choices=TNX_TYPE,
        max_length=20,
        blank=True,
        default='',
        help_text='The type of order transaction can be either Credit or Debit.'
    )
    mode = models.CharField(
        _('Transaction mode'),
        choices=TNX_MODE,
        max_length=20,
        blank=True,
        default='',
        help_text='The mode of the order transaction can be Offline, Cash On Delivery, Cheque, Draft, Wired, and Online.')
    status = models.CharField(
        _('Transaction status'),
        choices=TNX_STATUS,
        max_length=20,
        blank=True,
        default='',
        help_text='The status of the order transaction can be New, Cancelled, Failed, Pending, Declined, Rejected, and Success.'
    )
    summary = models.CharField(
        _('Summary'),
        max_length=225,
        blank=True,
        default='',
        help_text='The summary to mention the key highlights.'
    )

    class Meta:
        app_label = 'stock'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
