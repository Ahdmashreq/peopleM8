"""
WSGI config for MashreqPayroll project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MashreqPayroll.settings.production')

application = get_wsgi_application()
