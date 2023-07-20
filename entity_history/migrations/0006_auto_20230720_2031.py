# Generated by Django 3.2.20 on 2023-07-20 20:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity_history', '0005_auto_20180108_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entityactivationevent',
            name='creation_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow, help_text='The time that this entry was created'),
        ),
        migrations.AlterField(
            model_name='entityactivationevent',
            name='time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow, help_text='The time of the activation / deactivation'),
        ),
        migrations.AlterField(
            model_name='entityactivationevent',
            name='updated_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow, help_text='The time that this entry was updated'),
        ),
        migrations.AlterField(
            model_name='entityrelationshipactivationevent',
            name='creation_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow, help_text='The time that this entry was created'),
        ),
        migrations.AlterField(
            model_name='entityrelationshipactivationevent',
            name='time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow, help_text='The time of the activation / deactivation'),
        ),
        migrations.AlterField(
            model_name='entityrelationshipactivationevent',
            name='updated_time',
            field=models.DateTimeField(db_index=True, default=datetime.datetime.utcnow, help_text='The time that this entry was updated'),
        ),
    ]
