import os
import json

from django.conf import settings


def configure_settings():
    """
    Configures settings for manage.py and for run_tests.py.
    """
    if not settings.configured:
        # Determine the database settings depending on if a test_db var is set in CI mode or not
        test_db = os.environ.get('DB', None)
        if test_db is None:
            db_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': '',
                'HOST': 'db'
            }
        elif test_db == 'postgres':
            db_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'USER': 'postgres',
                'NAME': 'entity_history',
            }
        elif test_db == 'local':
            db_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'USER': 'postgres',
                'NAME': 'entity_history',
                'HOST': 'db'
            }
        elif test_db == 'sqlite':
            db_config = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'entity_history',
            }
        else:
            raise RuntimeError('Unsupported test DB {0}'.format(test_db))

        # Check env for db override (used for github actions)
        if os.environ.get('DB_SETTINGS'):
            db_config = json.loads(os.environ.get('DB_SETTINGS'))

        settings.configure(
            TEST_RUNNER='django_nose.NoseTestSuiteRunner',
            NOSE_ARGS=['--nocapture', '--nologcapture', '--verbosity=1'],
            DATABASES={
                'default': db_config,
            },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.admin',
                'entity',
                'entity_history',
                'entity_history.tests',
            ),
            ROOT_URLCONF='entity_history.urls',
            DEBUG=False,
            SECRET_KEY='12345',
            DEFAULT_AUTO_FIELD = 'django.db.models.AutoField',
            MIDDLEWARE=(
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'django.template.context_processors.request',
                    ]
                }
            }],
        )
