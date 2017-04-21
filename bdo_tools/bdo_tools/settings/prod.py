import os

from .base import BASE_DIR
from .base import *  # NOQA

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
