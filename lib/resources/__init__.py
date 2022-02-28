import json
import os
from types import SimpleNamespace

from django.conf import settings

from hakili.settings import cfg

libs = {}
files = []

for filename in os.listdir(settings.RESOURCES_DIR):
    if filename.endswith(".json"):
        cfg.read('{}'.format(filename))

        config_name = os.path.splitext(filename)[0]
        files.append(config_name)

        with open('{}/{}'.format(settings.RESOURCES_DIR, filename), 'r') as f:
            var = json.load(f)

            if config_name == 'api':
                api = json.dumps(var)
                var = json.loads(api, object_hook=lambda d: SimpleNamespace(**d))

        libs['{}'.format(config_name)] = var
