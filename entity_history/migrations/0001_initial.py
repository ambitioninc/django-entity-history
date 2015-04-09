# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityActivationEvent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('time', models.DateTimeField(db_index=True, help_text='The time of the activation / deactivation')),
                ('was_activated', models.BooleanField(help_text='True if the entity was activated, false otherwise', default=None)),
                ('entity', models.ForeignKey(help_text='The entity that was activated / deactivated', to='entity.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntityRelationshipActivationEvent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('time', models.DateTimeField(db_index=True, help_text='The time of the activation / deactivation')),
                ('was_activated', models.BooleanField(help_text='True if the entity was activated, false otherwise', default=None)),
                ('sub_entity', models.ForeignKey(to='entity.Entity', related_name='+', help_text='The sub entity in the relationship that was activated / deactivated')),
                ('super_entity', models.ForeignKey(to='entity.Entity', related_name='+', help_text='The super entity in the relationship that was activated / deactivated')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntityHistory',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('entity.entity',),
        ),
    ]
