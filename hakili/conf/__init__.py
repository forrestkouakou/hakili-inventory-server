from django.conf import settings

from .drf import *
from .email import *

if settings.DEBUG:
    from .logging import *
else:
    from .heroku_logging import *
