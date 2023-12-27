"""
WSGI config for price_comparison project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os



import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "price_comparison.settings")

application = get_wsgi_application()
application = WhiteNoise(application)
application.add_files(os.path.join(os.path.dirname(__file__), "comparer/static"), prefix="static/")

