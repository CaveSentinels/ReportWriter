"""
Django settings for BloodFinder project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from settings import *
import settings

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DEBUG = True


INSTALLED_APPS = settings.INSTALLED_APPS + (
    # 'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'enhanced_cwe2',
#         'USER': 'django',
#         'PASSWORD': 'django',
#         'HOST': 'localhost',
#     }
# }