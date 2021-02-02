import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)))
)
TEMPLATES_DIR = os.path.join(BASE_DIR, "MashreqPayroll", 'templates')
STATIC_DIR = os.path.join(BASE_DIR, "MashreqPayroll", "static")
MEDIA_DIR = os.path.join(BASE_DIR, "MashreqPayroll", "media")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
KEY_PATH = os.path.join(BASE_DIR, 'MashreqPayroll', 'django_key.txt')
with open(KEY_PATH) as f:
    SECRET_KEY = f.read().strip()

INSTALLED_APPS = [
    'custom_user.apps.CustomUserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'cities_light',
    'company',
    'djmoney',
    'currencies',
    'employee',
    'element_definition',
    'balanc_definition',
    'manage_payroll',
    'payroll_run',
    'defenition',
    'home',
    'leave',
    'attendance',
    'report',
    'recruitment',
    'service',
    'import_export',
    'mptt',
    'notifications',
    'task_management',
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'
IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'MashreqPayroll.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'home.middleware.PreventConcurrentLoginsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',

]

ROOT_URLCONF = 'MashreqPayroll.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',
            ],
        },
    },
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'MashreqPayroll.middleware.ForceDefaultLanguageMiddleware',
    'home.middleware.PreventConcurrentLoginsMiddleware',

)

WSGI_APPLICATION = 'MashreqPayroll.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
]

OPENEXCHANGERATES_APP_ID = "c2b2efcb306e075d9c2f2d0b614119ea"

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en', 'ar']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['EG', 'UAE', 'SA']
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en', 'ar']

# Login Url
LOGIN_REDIRECT_URL = 'home:homepage'
LOGIN_URL = '/home/login/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),
)


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = ["ar"]
LANGUAGE_CODE = 'en'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = '/mashreq_arabia/site/public/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    STATIC_DIR,
]

# Media files uploaded by user (images etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

AUTH_USER_MODEL = 'custom_user.User'


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "hr.mashreq.arabia@gmail.com"
EMAIL_HOST_PASSWORD = 'amrawy.gehad.mamdouh'
# with open(KEY_PATH) as f:
#     EMAIL_HOST_PASSWORD = f.read().strip()
EMAIL_USE_TLS = True
DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
