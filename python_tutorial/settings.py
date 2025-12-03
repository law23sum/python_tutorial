"""
Django settings for Python Tutorial project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote, urlparse, urlunparse

import environ
from corsheaders.defaults import default_headers
from django.utils.translation import gettext_lazy

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

RUNNING_IN_DOCKER = Path("/.dockerenv").exists()
DOCKER_DB_HOSTNAMES = {"db"}
DOCKER_REDIS_HOSTNAMES = {"redis"}


def _normalize_container_hostname(hostname, container_names):
    """Translate Docker-only hostnames to localhost when running natively."""

    if not hostname or RUNNING_IN_DOCKER:
        return hostname
    if hostname in container_names:
        return "localhost"
    return hostname


def _normalize_container_hostname_in_url(url_value, container_names):
    """Ensure URLs using Docker hostnames work when the app runs on the host OS."""

    if not url_value or RUNNING_IN_DOCKER:
        return url_value

    parsed = urlparse(url_value)
    if not parsed.hostname or parsed.hostname not in container_names:
        return url_value

    auth = ""
    if parsed.username is not None:
        auth = quote(parsed.username, safe="")
        if parsed.password is not None:
            auth = f"{auth}:{quote(parsed.password, safe='')}"
        auth = f"{auth}@"

    port = f":{parsed.port}" if parsed.port else ""
    new_netloc = f"{auth}localhost{port}"
    return urlunparse(parsed._replace(netloc=new_netloc))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-AclZAoyDMLfxbzOm5CSnj59OKf5CGIE5q0p4l0vY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)
ENABLE_DEBUG_TOOLBAR = env.bool("ENABLE_DEBUG_TOOLBAR", default=False) and "test" not in sys.argv

# Note: It is not recommended to set ALLOWED_HOSTS to "*" in production
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
]

# Put your third-party apps here
THIRD_PARTY_APPS = [
    "allauth",  # allauth account/registration management
    "allauth.account",
    "allauth.headless",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "django_watchfiles",
    "django_vite",
    "allauth.mfa",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    "rest_framework_api_key",
    "celery_progress",
    "hijack",  # "login as" functionality
    "hijack.contrib.admin",  # hijack buttons in the admin
    "djstripe",  # stripe integration
    "whitenoise.runserver_nostatic",  # whitenoise runserver
    "waffle",
    "health_check",
    "health_check.db",
    "health_check.contrib.celery",
    "health_check.contrib.redis",
    "django_celery_beat",
]

TUTORIAL_APPS = [
    "tutorial.apps.foundations.apps.FoundationsConfig",
    "tutorial.apps.data_structures.apps.DataStructuresConfig",
    "tutorial.apps.algorithms.apps.AlgorithmsConfig",
    "tutorial.apps.oop.apps.OopConfig",
    "tutorial.apps.patterns.apps.PatternsConfig",
    "tutorial.apps.web.apps.WebConfig",
    "tutorial.apps.topics.apps.TopicsConfig",
    "tutorial.apps.db.apps.DbConfig",
    "tutorial.apps.api.apps.ApiConfig",
    "tutorial.apps.async.apps.AsyncConfig",
    "tutorial.apps.devops.apps.DevopsConfig",
    "tutorial.apps.system_design.apps.SystemDesignConfig",
    "tutorial.apps.tests.apps.TestsConfig",
    "tutorial.apps.leadership.apps.LeadershipConfig",
]

# Put your project-specific apps here
PROJECT_APPS = [
    "apps.subscriptions.apps.SubscriptionConfig",
    "apps.users.apps.UserConfig",
    "apps.dashboard.apps.DashboardConfig",
    "apps.api.apps.APIConfig",
    "apps.utils",
    "apps.web",
    "apps.ai_images",
    "apps.chat",
    "apps.ai.apps.AiConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + TUTORIAL_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "apps.web.middleware.locale.UserLocaleMiddleware",
    "apps.web.middleware.locale.UserTimezoneMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "waffle.middleware.WaffleMiddleware",
]

if ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS.append("debug_toolbar")
    INTERNAL_IPS = ["127.0.0.1"]

if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "python_tutorial.urls"

# used to disable the cache in dev, but turn it on in production.
# more here: https://nickjanetakis.com/blog/django-4-1-html-templates-are-cached-by-default-with-debug-true
_DEFAULT_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

_CACHED_LOADERS = [("django.template.loaders.cached.Loader", _DEFAULT_LOADERS)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.web.context_processors.project_meta",
                # this line can be removed if not using google analytics
                "apps.web.context_processors.google_analytics_id",
            ],
            "loaders": _DEFAULT_LOADERS if DEBUG else _CACHED_LOADERS,
        },
    },
]

WSGI_APPLICATION = "python_tutorial.wsgi.application"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

if "DATABASE_URL" in env:
    database_config = env.db()
    normalized_host = _normalize_container_hostname(database_config.get("HOST"), DOCKER_DB_HOSTNAMES)
    if normalized_host:
        database_config["HOST"] = normalized_host
    DATABASES = {"default": database_config}
else:
    database_host = env("DJANGO_DATABASE_HOST", default="localhost")
    database_host = _normalize_container_hostname(database_host, DOCKER_DB_HOSTNAMES)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DJANGO_DATABASE_NAME", default="python_tutorial"),
            "USER": env("DJANGO_DATABASE_USER", default="postgres"),
            "PASSWORD": env("DJANGO_DATABASE_PASSWORD", default="***"),
            "HOST": database_host,
            "PORT": env("DJANGO_DATABASE_PORT", default="5432"),
        }
    }

# Auth and Login

# Django recommends overriding the user model even if you don"t think you need to because it makes
# future changes much easier.
AUTH_USER_MODEL = "users.CustomUser"
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/"

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

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

# Allauth setup

ACCOUNT_ADAPTER = "apps.users.adapter.EmailAsUsernameAdapter"
HEADLESS_ADAPTER = "apps.users.adapter.CustomHeadlessAdapter"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*"]

ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False  # don't send "forgot password" emails to unknown accounts
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
# This configures a honeypot field to prevent bots from signing up.
# The ID strikes a balance of "realistic" - to catch bots,
# and "not too common" - to not trip auto-complete in browsers.
# You can change the ID or remove it entirely to disable the honeypot.
ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = "phone_number_x"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
ACCOUNT_USER_DISPLAY = lambda user: user.get_display_name()  # noqa: E731

ACCOUNT_FORMS = {
    "signup": "apps.users.forms.TermsSignupForm",
}
SOCIALACCOUNT_FORMS = {
    "signup": "apps.users.forms.CustomSocialSignupForm",
}

FRONTEND_ADDRESS = env("FRONTEND_ADDRESS", default="http://localhost:5174")
USE_HEADLESS_URLS = env.bool("USE_HEADLESS_URLS", default=False)
if USE_HEADLESS_URLS:
    # These URLs will use the React front end instead of the Django views
    HEADLESS_FRONTEND_URLS = {
        "account_confirm_email": f"{FRONTEND_ADDRESS}/account/verify-email/{{key}}",
        "account_reset_password_from_key": f"{FRONTEND_ADDRESS}/account/password/reset/key/{{key}}",
        "account_signup": f"{FRONTEND_ADDRESS}/account/signup",
    }

# needed for cross-origin CSRF
CSRF_TRUSTED_ORIGINS = [FRONTEND_ADDRESS]
CSRF_COOKIE_DOMAIN = env("CSRF_COOKIE_DOMAIN", default=None)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (*default_headers, "x-password-reset-key", "x-email-verification-key")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[FRONTEND_ADDRESS])
SESSION_COOKIE_DOMAIN = env("SESSION_COOKIE_DOMAIN", default=None)

# User signup configuration: change to "mandatory" to require users to confirm email before signing in.
# or "optional" to send confirmation emails but not require them
ACCOUNT_EMAIL_VERIFICATION = env("ACCOUNT_EMAIL_VERIFICATION", default="none")

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# enable social login
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": env("GOOGLE_CLIENT_ID", default=""),
                "secret": env("GOOGLE_SECRET_ID", default=""),
                "key": "",
            },
        ],
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "github": {
        "APPS": [
            {
                "client_id": env("GITHUB_CLIENT_ID", default=""),
                "secret": env("GITHUB_SECRET_ID", default=""),
                "key": "",
            },
        ],
        "SCOPE": [
            "user",
        ],
    },
}

# For turnstile captchas
TURNSTILE_KEY = env("TURNSTILE_KEY", default=None)
TURNSTILE_SECRET = env("TURNSTILE_SECRET", default=None)


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"
LANGUAGE_COOKIE_NAME = "python_tutorial_language"
LANGUAGES = [
    ("en", gettext_lazy("English")),
    ("fr", gettext_lazy("French")),
]
LOCALE_PATHS = (BASE_DIR / "locale",)

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_ROOT = BASE_DIR / "static_root"
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # swap these to use manifest storage to bust cache when files change
        # note: this may break image references in sass/css files which is why it is not enabled by default
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Vite Integration
DJANGO_VITE = {
    "default": {
        "dev_mode": env.bool("DJANGO_VITE_DEV_MODE", default=DEBUG),
        "manifest_path": BASE_DIR / "static" / ".vite" / "manifest.json",
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

# future versions of Django will use BigAutoField as the default, but it can result in unwanted library
# migration files being generated, so we stick with AutoField for now.
# change this to BigAutoField if you"re sure you want to use it and aren"t worried about migrations.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Removes deprecation warning for future compatibility.
# see https://adamj.eu/tech/2023/12/07/django-fix-urlfield-assume-scheme-warnings/ for details.
FORMS_URLFIELD_ASSUME_HTTPS = True

# Email setup

# default email used by your server
SERVER_EMAIL = env("SERVER_EMAIL", default="noreply@0.0.0.0:8000")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="cswm7876@yahoo.com")

# The default value will print emails to the console, but you can change that here
# and in your environment.
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# Most production backends will require further customization. The below example uses Mailgun.
# ANYMAIL = {
#     "MAILGUN_API_KEY": env("MAILGUN_API_KEY", default=None),
#     "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN", default=None),
# }

# use in production
# see https://github.com/anymail/django-anymail for more details/examples
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

EMAIL_SUBJECT_PREFIX = "[Python Tutorial] "

# Marketing email configuration

# set these values if you want to subscribe people to a mailing list when they sign up.
MAILCHIMP_API_KEY = env("MAILCHIMP_API_KEY", default="")
MAILCHIMP_LIST_ID = env("MAILCHIMP_LIST_ID", default="")

# Django sites

SITE_ID = 1

# DRF config
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("apps.api.permissions.IsAuthenticatedOrHasUserAPIKey",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Python Tutorial",
    "DESCRIPTION": "The less boilerplate the better.",  # noqa: E501
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "displayOperationId": True,
    },
    "PREPROCESSING_HOOKS": [
        "apps.api.schema.filter_schema_apis",
    ],
    "APPEND_COMPONENTS": {
        "securitySchemes": {"ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "Authorization"}}
    },
    "SECURITY": [
        {
            "ApiKeyAuth": [],
        }
    ],
}
# Redis, cache, and/or Celery setup
if "REDIS_URL" in env:
    REDIS_URL = env("REDIS_URL")
elif "REDIS_TLS_URL" in env:
    REDIS_URL = env("REDIS_TLS_URL")
else:
    REDIS_HOST = env("REDIS_HOST", default="localhost")
    REDIS_HOST = _normalize_container_hostname(REDIS_HOST, DOCKER_REDIS_HOSTNAMES)
    REDIS_PORT = env("REDIS_PORT", default="6379")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

REDIS_URL = _normalize_container_hostname_in_url(REDIS_URL, DOCKER_REDIS_HOSTNAMES)

if REDIS_URL.startswith("rediss"):
    REDIS_URL = f"{REDIS_URL}?ssl_cert_reqs=none"

DUMMY_CACHE = {
    "BACKEND": "django.core.cache.backends.dummy.DummyCache",
}
REDIS_CACHE = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": REDIS_URL,
}
CACHES = {
    "default": DUMMY_CACHE if DEBUG else REDIS_CACHE,
}

CELERY_BROKER_URL = CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Add tasks to this dict and run `python manage.py bootstrap_celery_tasks` to create them
SCHEDULED_TASKS = {}

# Health Checks
# A list of tokens that can be used to access the health check endpoint
HEALTH_CHECK_TOKENS = env.list("HEALTH_CHECK_TOKENS", default="")


# Tutorial config

# replace any values below with specifics for your project
PROJECT_METADATA = {
    "NAME": gettext_lazy("Python Tutorial"),
    "URL": "http://0.0.0.0:8000",
    "DESCRIPTION": gettext_lazy("The less boilerplate the better."),  # noqa: E501
    "IMAGE": "https://upload.wikimedia.org/wikipedia/commons/2/20/PEO-pegasus_black.svg",
    "KEYWORDS": "SaaS, django",
    "CONTACT_EMAIL": "cswm7876@yahoo.com",
}

# set this to True in production to have URLs generated with https instead of http
USE_HTTPS_IN_ABSOLUTE_URLS = env.bool("USE_HTTPS_IN_ABSOLUTE_URLS", default=False)

ADMINS = [("Christian Dixon", "cswm7876@yahoo.com")]

# Add your google analytics ID to the environment to connect to Google Analytics
GOOGLE_ANALYTICS_ID = env("GOOGLE_ANALYTICS_ID", default="")

# these daisyui themes are used to set the dark and light themes for the site
# they must be valid themes included in your tailwind.config.js file.
# more here: https://daisyui.com/docs/themes/
LIGHT_THEME = "light"
DARK_THEME = "dark"

# Stripe config
# modeled to be the same as https://github.com/dj-stripe/dj-stripe
# Note: don"t edit these values here - edit them in your .env file or environment variables!
# The defaults are provided to prevent crashes if your keys don"t match the expected format.
STRIPE_LIVE_PUBLIC_KEY = env("STRIPE_LIVE_PUBLIC_KEY", default="pk_live_***")
STRIPE_LIVE_SECRET_KEY = env("STRIPE_LIVE_SECRET_KEY", default="sk_live_***")
STRIPE_TEST_PUBLIC_KEY = env("STRIPE_TEST_PUBLIC_KEY", default="pk_test_***")
STRIPE_TEST_SECRET_KEY = env("STRIPE_TEST_SECRET_KEY", default="sk_test_***")
# Change to True in production
STRIPE_LIVE_MODE = env.bool("STRIPE_LIVE_MODE", False)

# djstripe settings

DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"  # change to "djstripe_id" if not a new installation

SILENCED_SYSTEM_CHECKS = [
    "djstripe.I002",  # Pegasus uses the same settings as dj-stripe for keys, so don't complain they are here
]

if "test" in sys.argv:
    # Silence unnecessary warnings in tests
    SILENCED_SYSTEM_CHECKS.append("djstripe.I002")


# AI Image Setup
AI_IMAGES_STABILITY_AI_API_KEY = env("AI_IMAGES_STABILITY_AI_API_KEY", default="")
AI_IMAGES_OPENAI_API_KEY = env("AI_IMAGES_OPENAI_API_KEY", default="")

# AI Chat Setup
OPENAI_API_KEY = env("OPENAI_API_KEY", default="")
# LiteLLM models
# See:
# * https://docs.litellm.ai/docs/providers
# * https://docs.litellm.ai/docs/set_keys#litellm-variables
LLM_MODELS = {
    "gpt-5-nano": {"api_key": env("OPENAI_API_KEY", default="")},
    "gpt-4o": {"api_key": env("OPENAI_API_KEY", default="")},
    "claude-sonnet-4-5-20250929": {"api_key": env("ANTHROPIC_API_KEY", default="")},
    "ollama_chat/llama3": {"api_base": env("OLLAMA_API_BASE", default="http://localhost:11434")},
}
DEFAULT_LLM_MODEL = env("DEFAULT_LLM_MODEL", default="gpt-4o")
# see: https://ai.pydantic.dev/models/overview/ for model options
DEFAULT_AGENT_MODEL = env("DEFAULT_AGENT_MODEL", default="openai:gpt-4o")
if DEFAULT_LLM_MODEL not in LLM_MODELS:
    raise ValueError(f"DEFAULT_LLM_MODEL {DEFAULT_LLM_MODEL} not found in LLM_MODELS")


# Sentry setup

# populate this to configure sentry. should take the form: "https://****@sentry.io/12345"
SENTRY_DSN = env("SENTRY_DSN", default="")


if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": '[{asctime}] {levelname} "{name}" {message}',
            "style": "{",
            "datefmt": "%d/%b/%Y %H:%M:%S",  # match Django server time format
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
        },
        "python_tutorial": {
            "handlers": ["console"],
            "level": env("PYTHON_TUTORIAL_LOG_LEVEL", default="INFO"),
        },
        "tutorial": {
            "handlers": ["console"],
            "level": env("TUTORIAL_LOG_LEVEL", default=env("PEGASUS_LOG_LEVEL", default="DEBUG")),
        },
    },
}
