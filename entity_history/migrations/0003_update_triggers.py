# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from entity_history.sql.triggers import EntityActivationTrigger, EntityRelationshipActivationTrigger


def refresh_entity_activation_trigger(*args, **kwargs):
    EntityActivationTrigger().disable()
    EntityActivationTrigger().enable()


def refresh_entity_relationship_activation_trigger(*args, **kwargs):
    EntityRelationshipActivationTrigger().disable()
    EntityRelationshipActivationTrigger().enable()


class Migration(migrations.Migration):

    dependencies = [
        ('entity_history', '0002_auto_20150406_1605'),
    ]

    operations = [
        migrations.RunPython(
            code=refresh_entity_activation_trigger,
            reverse_code=refresh_entity_relationship_activation_trigger
        )
    ]
