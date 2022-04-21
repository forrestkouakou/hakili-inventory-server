from django.db import IntegrityError
from rest_framework.response import Response

from lib.config import django_logger


def http_return(status: bool, context: str, http_status: int):
    return Response({'status': status, 'context': context}, status=http_status)


def save_handler(klass_object):
    try:
        klass_object.save()
        klass_object.refresh_from_db()
        return klass_object
    except (IntegrityError, ValueError, KeyError) as e:
        django_logger.error("{}".format(e))
        return False
