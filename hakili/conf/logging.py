from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'development_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': settings.LOG_DIR / 'hakili_dev.log',
            'formatter': 'verbose'
        },
        'access_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.LOG_DIR / 'hakili_access.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'production_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.LOG_DIR / 'hakili_prod.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 5,
            'formatter': 'simple'
        },
        'dba_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.LOG_DIR / 'hakili_dba.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 5,
            'formatter': 'simple'
        },
    },
    'root': {
        'level': 'DEBUG',
        # 'handlers': ['console'],
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['dba_logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'coffeehouse': {
            'handlers': ['development_logfile', 'access_logfile', 'production_logfile'],
        },
        'django': {
            'handlers': ['development_logfile', 'access_logfile', 'production_logfile'],
        },
        'py.warnings': {
            'handlers': ['development_logfile', 'access_logfile'],
        },
    }
}
