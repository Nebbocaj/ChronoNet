# settings for production
# * inherits functionality from base.py

# ! some settings can cause problems without a certificate

from .base import *

# * this should NEVER be set to 'True' in this file
DEBUG = False

# This is for the AWS Apache instance
ALLOWED_HOSTS = ['www.khrono.space', 'khrono.space']

# redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# cookies can only be handled over HTTPS
SESSION_COOKIE_SECURE = True

# same as SESSION_COOKIE_SECURE but applies to CSRF token
CSRF_COOKIE_SECURE = True

# prevents javascript code from accessing csrf token creation
CSRF_COOKIE_HTTPONLY = True

# sets X-XSS-Protection: 1; mode=block header on all responses (script injection)
SECURE_BROWSER_XSS_FILTER = True

# http strict transport security header
SECURE_HSTS_SECONDS = 31536000  # one year

# subdomain protections
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'chronodb',
#         'USER': 'defaultUser',
#         'PASSWORD': '2beZSxLc3yg8gKXoLD2t'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypass'
    }
}

SITE_URL = 'khrono.space'

TIME_ZONE = 'America/Denver'