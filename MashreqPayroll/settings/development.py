import os
from MashreqPayroll.settings.base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
 }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'peoplem8',
#         'USER': 'mashreq_sysadmin',
#         'PASSWORD': 'M@$hreq123',
#         'HOST': '192.168.1.37',
#         'PORT': '',
#     }
# }
