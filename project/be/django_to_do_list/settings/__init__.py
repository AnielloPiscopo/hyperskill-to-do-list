import sys

from .local import *
from .auth import *
from .drf import *

if 'test' in sys.argv:
    REST_FRAMEWORK = {
        **REST_FRAMEWORK,
        'DEFAULT_THROTTLE_CLASSES': [],
        'DEFAULT_THROTTLE_RATES': {
            'anon': '10000/day',
            'user': '10000/day',
            'login': '10000/day',
        },
    }