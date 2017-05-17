from django.db import connection
from os.path import dirname


class EntityHistoryForeignKeys(object):
    def get_sql(self, name):
        return open(
            dirname(__file__) + '/' + name
        ).read()

    def enable_cascade_delete(self):
        with connection.cursor() as cursor:
            cursor.execute(self.get_sql('foreign_keys_cascade_delete.sql'))
