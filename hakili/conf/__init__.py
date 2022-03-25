from django.conf import settings

from .drf import *
from .email import *

if settings.DEBUG:
    from .logging import *

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
settings.DATABASES['default'].update(db_from_env)