# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('entity', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'EntityActivationEvent'
        db.create_table(u'entity_history_entityactivationevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity.Entity'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('was_activated', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'entity_history', ['EntityActivationEvent'])

        # Adding model 'EntityRelationshipActivationEvent'
        db.create_table(u'entity_history_entityrelationshipactivationevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['entity.Entity'])),
            ('super_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['entity.Entity'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('was_activated', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'entity_history', ['EntityRelationshipActivationEvent'])


    def backwards(self, orm):
        # Deleting model 'EntityActivationEvent'
        db.delete_table(u'entity_history_entityactivationevent')

        # Deleting model 'EntityRelationshipActivationEvent'
        db.delete_table(u'entity_history_entityrelationshipactivationevent')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'entity.entity': {
            'Meta': {'unique_together': "(('entity_id', 'entity_type', 'entity_kind'),)", 'object_name': 'Entity'},
            'display_name': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'blank': 'True'}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'entity_kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.EntityKind']"}),
            'entity_meta': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
        },
        u'entity.entitykind': {
            'Meta': {'object_name': 'EntityKind'},
            'display_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'})
        },
        u'entity_history.entityactivationevent': {
            'Meta': {'object_name': 'EntityActivationEvent'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'was_activated': ('django.db.models.fields.BooleanField', [], {})
        },
        u'entity_history.entityrelationshipactivationevent': {
            'Meta': {'object_name': 'EntityRelationshipActivationEvent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['entity.Entity']"}),
            'super_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['entity.Entity']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'was_activated': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['entity_history']
