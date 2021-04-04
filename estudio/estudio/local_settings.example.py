# pylint: disable=import-error,wildcard-import
from .settings import *  # noqa: F401,F403

DEBUG = True
SECRET_KEY = ""  # write your secret here!
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# pylint: disable=undefined-variable
LOGGING["root"]["level"] = "DEBUG"  # noqa: F405


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

# Sending email
# https://docs.djangoproject.com/en/3.1/topics/email/

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
