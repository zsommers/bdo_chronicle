import os

from .base import BASE_DIR, INSTALLED_APPS, TEMPLATES
from .base import *  # NOQA

DEBUG = True
django_template_settings = [x for x in TEMPLATES if x['BACKEND'] == 'django.template.backends.django.DjangoTemplates'][0]
django_template_settings['OPTIONS']['debug'] = True

MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INSTALLED_APPS += ['debug_toolbar']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
