from datetime import timedelta

from hakili.settings import env

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

REST_USE_JWT = env.bool('REST_USE_JWT')

JWT_AUTH_COOKIE = env.str('JWT_AUTH_COOKIE')
JWT_AUTH_REFRESH_COOKIE = env.str('JWT_AUTH_REFRESH_COOKIE')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKEN': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
