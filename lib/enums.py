from django.utils.translation import gettext as _
from model_utils import Choices

ACTIVATED = True
DEACTIVATED = False

STATE_CHOICES = Choices((ACTIVATED, _("Shown")), (DEACTIVATED, _("Hidden")))
# print("STATE_CHOICES ==> {}".format(STATE_CHOICES))
NULL = None
STATUS_CHOICES = Choices((NULL, _("Bocked")), (DEACTIVATED, "Deactivated"), (ACTIVATED, _("Activated")))

WEEK_DAY = Choices(
    ("monday", "Lundi"),
    ("tuesday", "Mardi"),
    ("wednesday", "Mercredi"),
    ("thursday", "Jeudi"),
    ("friday", "Vendredi"),
    ("saturday", "Samedi"),
    ("sunday", "Dimanche")
)

ORDER_STATUS = Choices(
    ("new", _("New")), ("checkout", _("Checkout")),
    ("paid", _("Paid")), ("failed", _("Failed")),
    ("shipped", _("Shipped")), ("delivered", _("Delivered")),
    ("returned", _("Returned")), ("complete", _("Complete"))
)

# TRANSACTION_TYPE = Choices(("credit", _("Credit")), ("debit", _("Debit")))

TRANSACTION_MODE = Choices(
    ("offline", _("Offline")), ("cash_on_delivery", _("Cash On Delivery")),
    ("cheque", _("Cheque")), ("draft", _("Draft")),
    ("wired", _("Wired")), ("online", _("Online"))
)

TRANSACTION_STATUS = Choices(
    ("new", _("New")), ("cancelled", _("Cancelled")),
    ("failed", _("Failed")), ("pending", _("Pending")),
    ("declined", _("Declined")), ("rejected", _("Rejected")),
    ("success", _("Success"))
)

PAYMENT_TYPE = Choices(
    ("cash", _("Cash")), ("transfer", _("Transfer")),
    ("card", _("Card")), ("check", _("Check"))
)
