import os
import random
import re
import string

import requests
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import get_current_user
from requests.adapters import HTTPAdapter
from rest_framework import serializers
from urllib3 import Retry

from lib.config import django_logger

app_name = __package__.split('.')[0]


class Hider(object):
    def __get__(self, instance, owner):
        raise AttributeError('Hidden attribute')

    def __set__(self, obj, val):
        raise AttributeError('Hidden attribute')


class Monitor(models.Model):
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_%(class)ss', editable=False)
    created_by = CurrentUserField(related_name='created_%(class)ss')
    # updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='updated_%(class)ss', editable=False)
    updated_by = CurrentUserField(related_name='updated_%(class)ss', on_update=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated:
            self.updated_by = user
            if not self.id:
                self.created_by = user
        super().save(*args, **kwargs)


class DynamicSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        # get the original representation
        ret = super(DynamicSerializer, self).to_representation(obj)

        # remove audit fields
        ret.pop('created_at')
        ret.pop('updated_at')
        ret.pop('created_by')
        ret.pop('updated_by')

        # here write the logic to check whether `elements` field is to be removed
        # pop 'elements' from 'ret' if condition is True

        # return the modified representation
        return ret


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    model = "{}".format(instance.__class__.__name__.lower())
    name = "{0}_{1}_{2}".format(model, instance.pk, generate_id())
    file = '{0}.{1}'.format(name, ext)
    path = os.path.join("uploads", model)
    return os.path.join(path, file)


def generate_string(size, return_type='string|pin'):
    chars = string.digits
    if return_type == 'string':
        chars += string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


def generate_id():
    import uuid
    return uuid.uuid4()


def requests_retry_session(
        retries=1,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


def api_call(url="", method="", data=None, timeout=15, retries=1, verify=False, auth=None):
    try:
        if data is None:
            data = {}

        if "headers" in data:
            headers = data["headers"]
        else:
            headers = {}

        if "params" in data:
            params = data["params"]
        else:
            params = {}

        django_logger.info("{0} => {1}".format(method, url))

        r = None

        if method:
            if method == 'GET':
                r = requests_retry_session(retries=retries).get(url, headers=headers, params=params, timeout=timeout,
                                                                verify=verify,
                                                                auth=auth)
            elif method == 'PUT':
                r = requests_retry_session(retries=retries).put(url, headers=headers, data=params, timeout=timeout,
                                                                verify=verify,
                                                                auth=auth)
            elif method == 'POST':
                r = requests_retry_session(retries=retries).post(url, headers=headers, data=params, timeout=timeout,
                                                                 verify=verify,
                                                                 auth=auth)
            elif method == 'DELETE':
                r = requests_retry_session(retries=retries).delete(url, headers=headers, timeout=timeout)

            # django_logger.info("{}".format(r))

        return r
    except requests.exceptions.ConnectionError as e:
        django_logger.error("Network problem occurred => {}".format(e))
        return {"status": False, "message": "{}".format(e)}
    except requests.exceptions.HTTPError as e:
        django_logger.error("Invalid HTTP response => {}".format(e))
        return {"status": False, "message": "{}".format(e)}
    except requests.exceptions.Timeout as e:
        django_logger.error("Oops ! The request has timed out => {}".format(e))
        return {"status": False, "message": "{}".format(e)}
    except requests.exceptions.RequestException as e:
        django_logger.error("An error occured => {}".format(e))
        return {"status": False, "message": "{}".format(e)}


def exec_api_call(url="", method="", headers=None, params=None, retries=0, timeout=15, scope='', verify=False,
                  auth=None):
    data = {}
    data["headers"] = headers
    data["params"] = params
    call = api_call(url, method, data, timeout=timeout, verify=verify, auth=auth)
    if "status" in call:
        return {}
    if not url_works(call.status_code):
        django_logger.error("==================== ERROR BEGIN ====================")
        django_logger.error("Scope : {} API".format(scope))
        django_logger.error("Method : {}".format(method))
        django_logger.error("URL : {}".format(url))
        django_logger.error("Headers : {}".format(headers))
        django_logger.error("Params : {}".format(params))
        django_logger.error("Status code : {} ({})".format(call.status_code, call.reason))
        django_logger.error("Return : {}".format(call.text))
        django_logger.error("==================== ERROR END ====================")
        return None
    django_logger.info("{} API : {} => {} ({})".format(scope, url, call.status_code, call.reason))
    return call.json()


def url_works(status_code):
    if 200 <= status_code < 400:
        return True
    else:
        return False


def py_slugify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single underscore
    s = re.sub(r"\s+", '_', s)

    return s


def dict_to_querydict(dictionary):
    from django.http import QueryDict
    from django.utils.datastructures import MultiValueDict

    qdict = QueryDict('', mutable=True)

    if type(dictionary) is dict:
        for key, value in dictionary.items():
            d = {key: value}
            qdict.update(MultiValueDict(d) if isinstance(value, list) else d)

    elif type(dictionary) is QueryDict:
        qdict.update(MultiValueDict(dictionary))

    return qdict
