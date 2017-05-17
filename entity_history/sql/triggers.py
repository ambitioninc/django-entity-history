from django.db import connection
from os.path import dirname


class SqlTrigger(object):
    trigger_procedure_create_name = None
    trigger_procedure_delete_name = None
    trigger_create_name = None
    trigger_delete_name = None

    def get_sql(self, name):
        return open(
            dirname(__file__) + '/' + name
        ).read()

    def enable(self):
        with connection.cursor() as cursor:
            cursor.execute(self.get_sql(self.trigger_procedure_create_name))
            cursor.execute(self.get_sql(self.trigger_create_name))

    def disable(self):
        with connection.cursor() as cursor:
            cursor.execute(self.get_sql(self.trigger_delete_name))
            cursor.execute(self.get_sql(self.trigger_procedure_delete_name))


class EntityActivationTrigger(SqlTrigger):
    trigger_procedure_create_name = 'entity_activation_procedure_create.sql'
    trigger_procedure_delete_name = 'entity_activation_procedure_delete.sql'
    trigger_create_name = 'entity_activation_trigger_create.sql'
    trigger_delete_name = 'entity_activation_trigger_delete.sql'


class EntityRelationshipActivationTrigger(SqlTrigger):
    trigger_procedure_create_name = 'entity_relationship_activation_procedure_create.sql'
    trigger_procedure_delete_name = 'entity_relationship_activation_procedure_delete.sql'
    trigger_create_name = 'entity_relationship_activation_trigger_create.sql'
    trigger_delete_name = 'entity_relationship_activation_trigger_delete.sql'

    def enable(self):
        raise Exception('This trigger is deprecated, use the immediate version')


class EntityRelationshipActivationImmediateTrigger(SqlTrigger):
    """
    This is an immediate version of the relationship activation trigger.
    """
    trigger_procedure_create_name = 'entity_relationship_activation_procedure_create.sql'
    trigger_procedure_delete_name = 'entity_relationship_activation_procedure_delete.sql'
    trigger_create_name = 'entity_relationship_activation_trigger_immediate_create.sql'
    trigger_delete_name = 'entity_relationship_activation_trigger_delete.sql'
