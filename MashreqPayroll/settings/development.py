import os
from MashreqPayroll.settings.base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'NAME': 'people_m8',
       'ENGINE': 'django.db.backends.mysql',
       'USER': 'root',
       'PASSWORD': '123/456/',
    },
   
}
