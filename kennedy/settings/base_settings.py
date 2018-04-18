"""Basic settings for Kennedy project"""
# pylint: disable=invalid-name
import os

import environ

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    APP_NAME=(str, 'kennedy-default'),
    TIME_ZONE=(str, 'US/Eastern'),
    LANGUAGE_CODE=(str, 'en-us'),
    KEY_PREFIX=(str, ''),
    CSRF_COOKIE_NAME=(str, 'kennedy_csrftoken'),
    SESSION_COOKIE_NAME=(str, 'kennedy_sessionid'),
    SESSION_ENGINE=(str, 'django.contrib.sessions.backends.cached_db'),
    SESSION_SERIALIZER=(
        str, 'django.contrib.sessions.serializers.JSONSerializer'),
    SESSION_EXPIRE_AT_BROWSER_CLOSE=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    SESSION_COOKIE_AGE=(int, 31536000),
    AWS_ACCESS_KEY_ID=(str, ''),
    AWS_SECRET_ACCESS_KEY=(str, ''),
    AWS_DEFAULT_REGION=(str, 'us-east-1'),
    DEFAULT_FROM_EMAIL=(str, 'Everyvoter <app@everyvoter.us>'),
    EMAIL_ACTIVE=(bool, False),
    SES_FEEDBACK_TOPIC_ARN=(str, ''),
    HIREFIRE_TOKEN=(str, ''),
    HIREFIRE_QUEUES=(list, ['celery']),
    DEBUG_TOOLBAR_IPS=(list, ['127.0.0.1']),
    CORS_ORIGIN_REGEX_WHITELIST=(tuple, (
        r'^(https?://)?(.+)\.ofa\.us$', r'^(https?://)?(.+)\.ofa\.us:8000$')),
    CORS_ORIGIN_WHITELIST=(list, ['localhost:8000', '127.0.0.1:8000']),
    SES_CONFIGURATIONSET_NAME=(str, 'everyvoter'),
    SECURE_SSL_REDIRECT=(bool, False)
)


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))



####
# Secret Key Settings

SECRET_KEY = env('SECRET_KEY')


####
# Core Application Settings

DEBUG = env('DEBUG')
ROOT_URLCONF = 'kennedy.urls'
WSGI_APPLICATION = 'kennedy.wsgi.application'
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')


#####
# Application name (i.e. `kennedy-prod`, `kennedy-staging`, etc)

APP_NAME = env('APP_NAME')


####
# Database Settings

DATABASES = {
    'default': env.db(),
}


#####
# Cache Settings

# Attempt to get the memcache info from Heroku.
try:
    # `django-heroku-memcachify` requires memcache to work. Since we only
    # need it on heroku and don't want to require libmemcached on dev
    # machines, we'll only use it if it's installed
    from memcacheify import memcacheify
    default_cache = memcacheify()['default']

    # memcacheify will use the LocMemCache if there is no heroku cache. So if
    # we see the 'LocMemCache' we know that memcachify is not running on a
    # heroku dyno that is setup for memcached
    # pylint: disable=line-too-long
    if default_cache['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache':
        default_cache = env.cache()

except ImportError:
    # If `django-heroku-memcachify` is not installed, just use the cache
    # defined in the environment
    default_cache = env.cache()

CACHES = {
    'default': default_cache,
}

KEY_PREFIX = env('KEY_PREFIX')


####
# Installed Apps Settings

INSTALLED_APPS = [
    'django.contrib.admin',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'corsheaders',

    'rest_framework',
    'django_filters',

    'crispy_forms',

    'django_celery_results',
    'django_celery_beat',

    # `django.contrib.auth` has to be after `accounts` because we override
    # `django.contrib.auth` management commands.
    'accounts',
    'django.contrib.auth',

    'manage',

    'api',
    'location',
    'branding',
    'election',
    'blocks',
    'mailer',
    'feedback',

    'user_import',

    'kennedy_common',

    'hirefire',

    'collectfast',
    'django.contrib.staticfiles',

    'django_nose',
    'clear_cache',

    'sekizai',

    'debug_toolbar'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'branding.middleware.BrandingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]


####
# Template settings

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'branding.context_processors.organization.organization'
            ]
        },

    },
]


####
# Custom authentication model setting
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'branding.auth_backends.BrandedBackend',)


####
# Authentication
LOGIN_URL = '/manage/login/'


####
# Session & CSRF Settings

CSRF_COOKIE_NAME = env('CSRF_COOKIE_NAME')
SESSION_COOKIE_NAME = env('SESSION_COOKIE_NAME')
SESSION_ENGINE = env('SESSION_ENGINE')
SESSION_SERIALIZER = env('SESSION_SERIALIZER')
SESSION_EXPIRE_AT_BROWSER_CLOSE = env('SESSION_EXPIRE_AT_BROWSER_CLOSE')
SESSION_COOKIE_AGE = env('SESSION_COOKIE_AGE')


####
# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


####
# File Upload Handling
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]


####
# API Settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'
}


####
# CORS Settings

# By default allow all *.ofa.us and *.ofa.us:8000 subdomains
CORS_ORIGIN_REGEX_WHITELIST = env('CORS_ORIGIN_REGEX_WHITELIST')

# Also allow some standard dev URLs
CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST')

####
# Amazon Web Services/Boto Settings
# AN AWS KEY IS NOT REQUIRED FOR DEVELOPMENT

# More configurations related to S3 can be found in `storage_settings.py` but
# since your code may rely on non-S3 parts of AWS it might be useful here.
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = env('AWS_DEFAULT_REGION')


####
# Email Server Settings
SES_CONFIGURATIONSET_NAME = env('SES_CONFIGURATIONSET_NAME')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_ACTIVE = env('EMAIL_ACTIVE')


####
# Email Feedback Settings
SES_FEEDBACK_TOPIC_ARN = env('SES_FEEDBACK_TOPIC_ARN')


####
# Geocod.io Key
GEOCODIO_KEY = env('GEOCODIO_KEY')


####
# HireFire Settings
HIREFIRE_TOKEN = env('HIREFIRE_TOKEN')
HIREFIRE_QUEUES = env('HIREFIRE_QUEUES')


####
# Timezone & Localization Settings
LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIME_ZONE')
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

USE_I18N = True
USE_L10N = True
USE_TZ = True


###
# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


####
# Test Runner Settings

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--nologcapture'
]


####
# Django Debug Toolbar Settings

INTERNAL_IPS = env('DEBUG_TOOLBAR_IPS')

