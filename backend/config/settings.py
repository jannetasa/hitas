import os

import environ
from django.utils.translation import gettext_lazy as _

# Set up .env
root = environ.Path(__file__) - 2
assert os.path.exists(root("manage.py"))
var_root = root("var")

BASE_DIR = root()

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, None),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, "postgres:///hitas"),
    VAR_ROOT=(str, var_root),
    STATIC_URL=(str, "/static/"),
    MEDIA_URL=(str, "/media/"),
)
env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

var_root = env.path("VAR_ROOT")
STATIC_ROOT = var_root("static")
MEDIA_ROOT = var_root("media")
STATIC_URL = env("STATIC_URL")
MEDIA_URL = env("MEDIA_URL")

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "helusers.apps.HelusersConfig",
    "helusers.apps.HelusersAdminConfig",
    "users",
    "hitas",
    "nested_inline",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "crum.CurrentRequestUserMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEST_RUNNER = "hitas.tests.runner.HitasDatabaseRunner"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "hitas.exceptions.exception_handler",
    "COERCE_DECIMAL_TO_STRING": False,
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/login/"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "fi"
LANGUAGES = [
    ("fi", _("Finnish")),
    ("en", _("English")),
]
LOCALE_PATHS = ["./templates/locale"]

TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_L10N = True
USE_TZ = True

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
