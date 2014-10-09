Installation
============

To install the latest release, type::

    pip install django-entity-history

To install the latest code directly from source, type::

    pip install git+git://github.com/ambitioninc/django-entity-history.git

Add `entity_history` to your installed Django apps in your project settings. Note that `entity` will also need to be in the installed apps.

Run `python manage.py migrate` and the postgres database triggers that track entity events will be installed.