# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        # Create the trigger for entity events
        db.execute(
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
        db.execute(
            'CREATE TRIGGER update_entity_activation_history AFTER INSERT OR UPDATE OF is_active ON entity_entity\n'
            '    FOR EACH ROW EXECUTE PROCEDURE update_entity_activation_history();'
        )

        # Create the trigger for entity relationship events
        db.execute(
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
        db.execute(
            'CREATE CONSTRAINT TRIGGER update_entity_relationship_activation_history AFTER INSERT OR DELETE ON entity_entityrelationship\n'
            'INITIALLY DEFERRED FOR EACH ROW EXECUTE PROCEDURE update_entity_relationship_activation_history();'
        )


    def backwards(self, orm):
        db.execute(
            'DROP TRIGGER update_entity_activation_history ON entity_entity;'
        )
        db.execute(
            'DROP FUNCTION update_entity_activation_history();'
        )

        db.execute(
            'DROP TRIGGER update_entity_relationship_activation_history ON entity_entityrelationship;'
        )
        db.execute(
            'DROP FUNCTION update_entity_relationship_activation_history();'
        )

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
    symmetrical = True
