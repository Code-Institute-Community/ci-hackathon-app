import os

from django.core.management.utils import get_random_secret_key
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from dotenv import load_dotenv

ENV_FILE = os.getenv('ENV_FILE', '.env')

if ENV_FILE:
    load_dotenv(ENV_FILE)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = "DEVELOPMENT" in os.environ

ALLOWED_HOSTS = []
host = os.environ.get("SITE_NAME", '*')
if host:
    ALLOWED_HOSTS.append(host)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",

    # custom apps
    "accounts",
    "hackathon",
    "hackadmin",
    "home",
    "images",
    "profiles",
    "resources",
    "showcase",
    "teams",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "main.urls"

CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # required by allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "crispy_forms.templatetags.crispy_forms_tags",
                "crispy_forms.templatetags.crispy_forms_field",
            ]
        },
    },
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTH_USER_MODEL = "accounts.CustomUser"
ACCOUNT_SIGNUP_FORM_CLASS = "accounts.forms.SignupForm"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/post_login/"


WSGI_APPLICATION = "main.wsgi.application"

if not DEBUG:
    DATABASES = {
        'default': {
            'ATOMIC_REQUESTS': True,
            'CONN_MAX_AGE': 0,
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.getenv('DBHOST'),  # '127.0.0.1',
            'NAME': os.getenv('DBNAME'),  #'hackathons',
            'OPTIONS': {},
            'PASSWORD': os.getenv('DBPASS'),
            'PORT': os.getenv('DBPORT', '3306'),
            'USER': os.getenv('DBUSER'),
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "data", "db.sqlite3"),
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_LOCATION = "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIAFILES_LOCATION = "media"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
SLACK_ENABLED = os.environ.get("SLACK_ENABLED") == 'True'

if SLACK_ENABLED:
    SLACK_WORKSPACE = os.environ.get('SLACK_WORKSPACE')
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    INSTALLED_APPS += ['custom_slack_provider']
    SOCIALACCOUNT_PROVIDERS = {
        'custom_slack_provider': {
            'SCOPE':['identity.basic', 'identity.email'],
        }
    }

SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )
