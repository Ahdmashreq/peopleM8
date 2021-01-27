import os
from MashreqPayroll.settings.base import *


DEBUG = True

ADMINS = [('ahd','ahd.hozayen@mashreqarabia.com')]

ALLOWED_HOSTS = ['127.0.0.1','127.0.1.1','165.22.19.247', '192.168.1.37']

TIMEOUT = 900

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'peoplem8',
        'USER': 'mashreq_sysadmin',
        'PASSWORD': 'M@$hreq123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# to end the user session when closing the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 43200      # session cookie timeout is 12 hours
