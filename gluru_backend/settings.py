"""
Django settings for gluru_backend project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import environ
root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
HTTPS = env.bool('HTTPS', False)

if HTTPS:
    PROTOCOL = 'https'
else:
    PROTOCOL = 'http'

SITE_ID = 1

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'haystack',
    'corsheaders',
    'fieldsignals',
    'profiles.apps.ProfilesConfig',
    'tickets.apps.TicketsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gluru_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(root.path('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gluru_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if env.str('DATABASE_URL', default=''):
    DATABASES = {
        'default': env.db(),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': root('db.sqlite3'),
        },
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Settings Realted To Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '[%(levelname)s] [%(asctime)s] [%(funcName)s line: %(lineno)d] - %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#         'log_file': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': root('logs/django.log'),
#             'maxBytes': '16777216',  # 16Mb
#             'formatter': 'verbose'
#         },
#         'crm_log': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': root('logs/crm.log'),
#             'maxBytes': '16777216',  # 16Mb
#             'formatter': 'verbose'
#         },
#         'email_log': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': root('logs/email.log'),
#             'maxBytes': '16777216',  # 16Mb
#             'formatter': 'verbose'
#         },
#         'idp_log': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': root('logs/idp.log'),
#             'maxBytes': '16777216',  # 16Mb
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['log_file', 'console'],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#         'crm': {
#             'handlers': ['crm_log'],
#             'level': 'INFO'
#         },
#         'emails': {
#             'handlers': ['email_log'],
#             'level': 'INFO'
#         },
#         'idp': {
#             'handlers': ['idp_log'],
#             'level': 'INFO'
#         },
#     }
# }

AUTH_USER_MODEL = 'profiles.User'

# Settings Realted To Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}


# Settings Related To Twilio
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN')


# Email Settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_FROM = env('EMAIL_FROM')


# Account Management App Settings
USER_INFO_FETCH_ENDPOINT = env('USER_INFO_FETCH_ENDPOINT')
COMPANY_INFO_FETCH_ENDPOINT = env('COMPANY_INFO_FETCH_ENDPOINT')


# Haystack Settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': str(root.path('whoosh_index')),
    },
}
