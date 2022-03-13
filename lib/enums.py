from django.utils.translation import gettext as _
from model_utils import Choices

ACTIVATED = True
DEACTIVATED = False

STATE_CHOICES = Choices((ACTIVATED, _("Shown")), (DEACTIVATED, _("Hidden")))
# print("STATE_CHOICES ==> {}".format(STATE_CHOICES))
NULL = None
STATUS_CHOICES = Choices((NULL, _("Bocked")), (DEACTIVATED, "Deactivated"), (ACTIVATED, _("Activated")))

MONDAY = "monday"
TUESDAY = "tuesday"
WEDNESDAY = "wednesday"
THURSDAY = "thursday"
FRIDAY = "friday"
SATURDAY = "saturday"
SUNDAY = "sunday"

WEEK_DAY = Choices(
    (MONDAY, "Lundi"),
    (TUESDAY, "Mardi"),
    (WEDNESDAY, "Mercredi"),
    (THURSDAY, "Jeudi"),
    (FRIDAY, "Vendredi"),
    (SATURDAY, "Samedi"),
    (SUNDAY, "Dimanche")
)

PAYMENT_TYPE = Choices(("cash", _("Cash")), ("transfer", _("Transfer")), ("card", _("Card")), "check", _("Check"))
PAYMENT_STATUS = Choices(("cash", _("Cash")), ("transfer", _("Transfer")), ("card", _("Card")), "check", _("Check"))
ORDER_STATUS = Choices(("new", _("New")), ("checkout", _("Checkout")), ("paid", _("Paid")), ("failed", _("Failed")), ("shipped", _("Shipped")), ("delivered", _("Delivered")), ("returned", _("Returned")), ("complete", _("Complete")))
