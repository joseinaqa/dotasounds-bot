import dj_database_url
import os

INSTALLED_APPS = [
    'app',
    'django.contrib.postgres',
]

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True),
}

SECRET_KEY = os.environ['SECRET_KEY']
