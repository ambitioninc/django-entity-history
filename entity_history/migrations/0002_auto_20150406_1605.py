# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Forwards(object):

    CREATE_FUNCTION_ACTIVATION = (
        'CREATE OR REPLACE FUNCTION update_entity_activation_history()\n'
        '    RETURNS trigger AS\n'
        '$BODY$\n'
        'BEGIN\n'
        '\n'
        'IF (TG_OP = \'INSERT\' OR (TG_OP = \'UPDATE\' AND OLD.is_active != NEW.is_active)) THEN\n'
        '    INSERT INTO entity_history_entityactivationevent(entity_id, time, was_activated)\n'
        '    VALUES (NEW.id, CAST(CLOCK_TIMESTAMP() at time zone \'utc\' AS timestamp), NEW.is_active);\n'
        'END IF;\n'
        '\n'
        'RETURN NEW;\n'
        'END;\n'
        '$BODY$\n'
        'LANGUAGE plpgsql VOLATILE;\n'
    )
    CREATE_TRIGGER_ACTIVATION = (
        'CREATE TRIGGER update_entity_activation_history AFTER INSERT OR UPDATE OF is_active ON entity_entity\n'
        '    FOR EACH ROW EXECUTE PROCEDURE update_entity_activation_history();'
    )
    CREATE_FUNCTION_RELATIONSHIP = (
        'CREATE OR REPLACE FUNCTION update_entity_relationship_activation_history()\n'
        '    RETURNS trigger AS\n'
        '$BODY$\n'
        'BEGIN\n'
        '\n'
        '    IF (TG_OP = \'INSERT\') THEN\n'
        '        INSERT INTO entity_history_entityrelationshipactivationevent(sub_entity_id, super_entity_id, time, was_activated)\n'
        '        VALUES (NEW.sub_entity_id, NEW.super_entity_id, CAST(CLOCK_TIMESTAMP() at time zone \'utc\' AS timestamp), \'true\');\n'
        '    END IF;\n'
        '\n'
        '    IF (TG_OP = \'DELETE\') AND (SELECT COUNT(*) FROM entity_entity WHERE id IN (OLD.sub_entity_id, OLD.super_entity_id)) = 2 THEN\n'
        '        INSERT INTO entity_history_entityrelationshipactivationevent(sub_entity_id, super_entity_id, time, was_activated)\n'
        '        VALUES (OLD.sub_entity_id, OLD.super_entity_id, CAST(CLOCK_TIMESTAMP() at time zone \'utc\' AS timestamp), \'false\');\n'
        '    END IF;\n'
        '\n'
        '    RETURN NEW;\n'
        'END;\n'
        '$BODY$\n'
        'LANGUAGE plpgsql VOLATILE;\n'
    )
    CREATE_TRIGGER_RELATIONSHIP = (
        'CREATE CONSTRAINT TRIGGER update_entity_relationship_activation_history AFTER INSERT OR DELETE ON entity_entityrelationship\n'
        'INITIALLY DEFERRED FOR EACH ROW EXECUTE PROCEDURE update_entity_relationship_activation_history();'
    )


class Backwards(object):
    DROP_TRIGGER_RELATIONSHIP = (
        'DROP TRIGGER update_entity_relationship_activation_history ON entity_entityrelationship;'
    )
    DROP_FUNCTION_RELATIONSHIP = (
        'DROP FUNCTION update_entity_relationship_activation_history();'
    )
    DROP_TRIGGER_ACTIVATION = (
        'DROP TRIGGER update_entity_activation_history ON entity_entity;'
    )
    DROP_FUNCTION_ACTIVATION = (
        'DROP FUNCTION update_entity_activation_history();'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('entity_history', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=Forwards.CREATE_FUNCTION_ACTIVATION,
            reverse_sql=Backwards.DROP_FUNCTION_ACTIVATION,
        ),
        migrations.RunSQL(
            sql=Forwards.CREATE_TRIGGER_ACTIVATION,
            reverse_sql=Backwards.DROP_TRIGGER_ACTIVATION
        ),
        migrations.RunSQL(
            sql=Forwards.CREATE_FUNCTION_RELATIONSHIP,
            reverse_sql=Backwards.DROP_FUNCTION_RELATIONSHIP
        ),
        migrations.RunSQL(
            sql=Forwards.CREATE_TRIGGER_RELATIONSHIP,
            reverse_sql=Backwards.DROP_TRIGGER_RELATIONSHIP
        ),
    ]
