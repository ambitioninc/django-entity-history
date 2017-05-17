from datetime import datetime

from django.db import connection
from django.test import TransactionTestCase
from django_dynamic_fixture import G
from entity.models import Entity
from entity_history.models import EntityRelationshipActivationEvent, EntityActivationEvent


class CascadeDeleteTest(TransactionTestCase):
    def test_cascade_delete(self):
        # Create some entities and events
        super_e1 = G(Entity)
        super_e2 = G(Entity)
        sub_e1 = G(Entity)
        sub_e2 = G(Entity)

        G(EntityActivationEvent, was_activated=True, entity=super_e1, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=True, entity=super_e2, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=True, entity=sub_e1, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=True, entity=sub_e2, time=datetime(2013, 2, 1))

        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e1, sub_entity=sub_e1,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e1, sub_entity=sub_e1,
            time=datetime(2013, 2, 3))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e1, sub_entity=sub_e1,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e1, sub_entity=sub_e1,
            time=datetime(2013, 2, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e1, sub_entity=sub_e1,
            time=datetime(2013, 3, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e2, sub_entity=sub_e1,
            time=datetime(2013, 1, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e2, sub_entity=sub_e1,
            time=datetime(2013, 12, 1))

        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e1, sub_entity=sub_e2,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e1, sub_entity=sub_e2,
            time=datetime(2013, 2, 20))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e1, sub_entity=sub_e2,
            time=datetime(2013, 3, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e1, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e1, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 13))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e2, sub_entity=sub_e2,
            time=datetime(2013, 1, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e2, sub_entity=sub_e2,
            time=datetime(2013, 12, 1))

        # Run the delete outside of django
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM entity_entity')

        # Check that all tables are empty
        self.assertEqual(Entity.objects.all().count(), 0)
        self.assertEqual(EntityRelationshipActivationEvent.objects.all().count(), 0)
        self.assertEqual(EntityActivationEvent.objects.all().count(), 0)
