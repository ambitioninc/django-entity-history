# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from entity_history.sql.foreign_keys import EntityHistoryForeignKeys
from entity_history.sql.triggers import (
    EntityActivationTrigger,
    EntityRelationshipActivationImmediateTrigger
)


def refresh_entity_activation_trigger(*args, **kwargs):
    EntityActivationTrigger().disable()
    EntityActivationTrigger().enable()


def refresh_entity_relationship_activation_trigger(*args, **kwargs):
    EntityRelationshipActivationImmediateTrigger().disable()
    EntityRelationshipActivationImmediateTrigger().enable()


def update_foreign_keys(*args, **kwargs):
    EntityHistoryForeignKeys().enable_cascade_delete()


class Migration(migrations.Migration):

    dependencies = [
        ('entity_history', '0003_update_triggers'),
    ]

    operations = [
        migrations.RunPython(
            code=refresh_entity_activation_trigger,
        ),
        migrations.RunPython(
            code=refresh_entity_relationship_activation_trigger
        ),
        migrations.RunPython(
            code=update_foreign_keys
        )
    ]
