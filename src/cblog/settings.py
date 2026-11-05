
"""
Django settings for cblog project.
"""

from pathlib import Path

import boto3
from decouple import config


# --------------------------------------------------
# Base configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1"
).split(",")


# --------------------------------------------------
# Applications
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # My applications
    "blog.apps.BlogConfig",
    "users.apps.UsersConfig",

    # Third-party applications
    "crispy_forms",
    "crispy_bootstrap4",
    "storages",
]


# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "cblog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "cblog.wsgi.application"


# --------------------------------------------------
# AWS configuration
# --------------------------------------------------

AWS_REGION = config("AWS_REGION", default="us-east-1")

AWS_STORAGE_BUCKET_NAME = config(
    "AWS_STORAGE_BUCKET_NAME",
    default="awscapstonesguilesblog"
)

AWS_S3_REGION_NAME = AWS_REGION

AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3."
    f"{AWS_S3_REGION_NAME}.amazonaws.com"
)


# No ACLs; bucket policy controls public reads
AWS_DEFAULT_ACL = None

AWS_QUERYSTRING_AUTH = False

AWS_S3_FILE_OVERWRITE = False


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

ssm = boto3.client("ssm", region_name=AWS_REGION)


def get_ssm_parameter(name):
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response["Parameter"]["Value"]


db_username = get_ssm_parameter("/guile/capstone/username")
db_password = get_ssm_parameter("/guile/capstone/password")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME", default="ondia"),
        "USER": db_username,
        "PASSWORD": db_password,
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# --------------------------------------------------
# Password validation
# --------------------------------------------------

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


# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# Static and media files
# --------------------------------------------------

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


STORAGES = {
    "default": {
        "BACKEND": "cblog.storages.MediaStore",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "static",
        },
    },
}


# --------------------------------------------------
# Crispy forms
# --------------------------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap4"]

CRISPY_TEMPLATE_PACK = "bootstrap4"


# --------------------------------------------------
# Authentication
# --------------------------------------------------

LOGIN_REDIRECT_URL = "blog:list"

LOGIN_URL = "login"


# --------------------------------------------------
# Default primary key
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
