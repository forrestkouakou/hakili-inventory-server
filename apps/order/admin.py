from django.apps import apps
from django.contrib import admin

for model in apps.get_app_config('order').models.values():
    admin.site.register(model)
