"""
Django settings for HMS (Hospital Management System)
"""

from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='your-secret-key-change-in-production')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    """
    Django settings for HMS (Hospital Management System)
    """

    from pathlib import Path
    import os
    from decouple import config
    import dj_database_url

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = config('DJANGO_SECRET_KEY', default='your-secret-key-change-in-production')

    # Set DEBUG via environment variable in production
    DEBUG = config('DEBUG', default=True, cast=bool)

    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
        'hms_app',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'hms_project.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
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

    WSGI_APPLICATION = 'hms_project.wsgi.application'

    # Database: allow DATABASE_URL override (e.g., provided by Vercel or Railway)
    DATABASE_URL = config('DATABASE_URL', default='')
    if DATABASE_URL:
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', default='hms_db'),
                'USER': config('DB_USER', default='postgres'),
                'PASSWORD': config('DB_PASSWORD', default='password'),
                'HOST': config('DB_HOST', default='localhost'),
                'PORT': config('DB_PORT', default='5432'),
            }
        }

    # Password validation
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
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    # Static files
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = [BASE_DIR / 'static']
    # WhiteNoise static files storage for production
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Default primary key field type
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # REST Framework settings
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

    # CORS settings
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]

    # Email settings (for serverless integration)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Media files (uploads)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

    # Optional S3 storage for media when deploying to cloud
    USE_S3 = config('USE_S3', default=False, cast=bool)
    if USE_S3:
        # Configure django-storages with S3
        AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
        AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default=None)
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
        