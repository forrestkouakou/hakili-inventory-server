from django.utils.translation import gettext as _
from model_utils import Choices

ACTIVATED = True
DEACTIVATED = False

STATE_CHOICES = Choices((ACTIVATED, _("Shown")), (DEACTIVATED, _("Hidden")))

NULL = None
STATUS_CHOICES = ((NULL, _("Null")), (DEACTIVATED, "Deactivated"), (ACTIVATED, _("Activated")))

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
