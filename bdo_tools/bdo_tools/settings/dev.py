from .base import *

DEBUG = True
django_template_settings = [x for x in TEMPLATES if x['BACKEND'] == 'django.template.backends.django.DjangoTemplates'][0]
django_template_settings['OPTIONS']['debug'] = True

INSTALLED_APPS += ['debug_toolbar']