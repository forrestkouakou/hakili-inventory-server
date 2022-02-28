import logging

from hakili.settings import env

APP_NAME = env.str('APP_NAME')

django_logger = logging.getLogger('django')

default_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
