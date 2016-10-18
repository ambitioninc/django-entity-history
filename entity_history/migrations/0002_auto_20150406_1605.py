# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from entity_history.sql.triggers import EntityActivationTrigger, EntityRelationshipActivationTrigger


def enable_entity_activation_trigger(*args, **kwargs):
    EntityActivationTrigger().enable()


def disable_entity_activation_trigger(*args, **kwargs):
    EntityActivationTrigger().disable()


def enable_entity_relationship_activation_trigger(*args, **kwargs):
    EntityRelationshipActivationTrigger().enable()


def disable_entity_relationship_activation_trigger(*args, **kwargs):
    EntityRelationshipActivationTrigger().disable()


class Migration(migrations.Migration):

    dependencies = [
        ('entity_history', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=enable_entity_activation_trigger,
            reverse_code=disable_entity_activation_trigger
        ),
        migrations.RunPython(
            code=enable_entity_relationship_activation_trigger,
            reverse_code=disable_entity_relationship_activation_trigger
        )
    ]
