from .base import *
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = ['*']

# Database
# Using SQLite for local development by default (from base.py)
# If using Postgres locally (e.g. via Docker), override here if DATABASE_URL is set
if config('DATABASE_URL', default=None):
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=False
        )
    }

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging
# Log to console
LOGGING['handlers']['console']['level'] = 'DEBUG'
