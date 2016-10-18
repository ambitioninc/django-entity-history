from datetime import datetime

from django.test import TransactionTestCase
from django_dynamic_fixture import G, N
from entity.models import EntityRelationship, Entity

from entity_history.models import EntityRelationshipActivationEvent


class EntityRelationshipActivationTriggerTests(TransactionTestCase):
    """
    Tests that entity activation events are properly created when entities
    are activated and deactivated. This is accomplished by a postgres database
    trigger that is installed in a data migration.
    """
    def test_relationship_cascade_delete(self):
        """
        Tests the case when an entity is deleted, which causes the relationship to
        be cascaded. This should result in no history being stored since the entity
        is no longer present.
        """
        e = G(Entity)
        G(EntityRelationship, super_entity=e)
        e.delete(force=True)

        self.assertFalse(Entity.objects.filter(id=e.id).exists())
        self.assertFalse(EntityRelationshipActivationEvent.objects.exists())

    def test_bulk_create(self):
        ers = [N(EntityRelationship) for i in range(3)]
        t1 = datetime.utcnow()
        EntityRelationship.objects.bulk_create(ers)
        t2 = datetime.utcnow()

        events = list(EntityRelationshipActivationEvent.objects.all())
        self.assertEquals(len(events), 3)
        for i in range(3):
            self.assertTrue(events[i].was_activated)
            self.assertTrue(t1 <= events[i].time <= t2)

    def test_bulk_create_delete(self):
        ers = [N(EntityRelationship) for i in range(3)]
        t1 = datetime.utcnow()
        EntityRelationship.objects.bulk_create(ers)
        t2 = datetime.utcnow()
        EntityRelationship.objects.all().delete()
        t3 = datetime.utcnow()

        events = list(EntityRelationshipActivationEvent.objects.all())
        self.assertTrue(len(events), 3)
        for i in range(3):
            self.assertTrue(events[i].was_activated)
            self.assertTrue(t1 <= events[i].time <= t2)
        for i in range(3, 6):
            self.assertFalse(events[i].was_activated)
            self.assertTrue(t2 <= events[i].time <= t3)

    def test_entity_relationship_creation(self):
        t1 = datetime.utcnow()
        er = G(EntityRelationship)
        t2 = datetime.utcnow()

        event = EntityRelationshipActivationEvent.objects.get()
        self.assertTrue(event.was_activated)
        self.assertEquals(event.sub_entity, er.sub_entity)
        self.assertEquals(event.super_entity, er.super_entity)
        self.assertTrue(t1 <= event.time <= t2)

    def test_entity_relationship_creation_deletion(self):
        t1 = datetime.utcnow()
        er = G(EntityRelationship)
        sub_entity = er.sub_entity
        super_entity = er.super_entity
        t2 = datetime.utcnow()
        er.delete()
        t3 = datetime.utcnow()

        events = list(EntityRelationshipActivationEvent.objects.order_by('time', 'id'))

        self.assertTrue(events[0].was_activated)
        self.assertEquals(events[0].sub_entity, sub_entity)
        self.assertEquals(events[0].super_entity, super_entity)
        self.assertTrue(t1 <= events[0].time <= t2)

        self.assertFalse(events[1].was_activated)
        self.assertEquals(events[1].sub_entity, sub_entity)
        self.assertEquals(events[1].super_entity, super_entity)
        self.assertTrue(t2 <= events[1].time <= t3)

    def test_entity_relationship_creation_deletion_creation_save(self):
        t1 = datetime.utcnow()
        er = G(EntityRelationship)
        sub_entity1 = er.sub_entity
        super_entity1 = er.super_entity
        t2 = datetime.utcnow()
        er.delete()
        t3 = datetime.utcnow()
        er = G(EntityRelationship)
        sub_entity2 = er.sub_entity
        super_entity2 = er.super_entity
        er.save()
        t4 = datetime.utcnow()

        events = list(EntityRelationshipActivationEvent.objects.order_by('time', 'id'))

        self.assertTrue(events[0].was_activated)
        self.assertEquals(events[0].sub_entity, sub_entity1)
        self.assertEquals(events[0].super_entity, super_entity1)
        self.assertTrue(t1 <= events[0].time <= t2)

        self.assertFalse(events[1].was_activated)
        self.assertEquals(events[1].sub_entity, sub_entity1)
        self.assertEquals(events[1].super_entity, super_entity1)
        self.assertTrue(t2 <= events[1].time <= t3)

        self.assertTrue(events[2].was_activated)
        self.assertEquals(events[2].sub_entity, sub_entity2)
        self.assertEquals(events[2].super_entity, super_entity2)
        self.assertTrue(t3 <= events[2].time <= t4)

    def test_entity_relationship_duplicated(self):
        """
        Test the case when a relationship of the same entities is created multiple times.
        This should not happen, but lets guard against it anyways
        """

        # Create the relation
        entity_relation = G(EntityRelationship)

        # Create a duplicate relation
        G(
            EntityRelationship,
            sub_entity=entity_relation.sub_entity,
            super_entity=entity_relation.super_entity
        )

        # We should only have one event
        event = EntityRelationshipActivationEvent.objects.get()
        self.assertTrue(event.was_activated)

        # Delete the relations
        EntityRelationship.objects.all().delete()

        # Assert that we only have one unactivated event
        events = EntityRelationshipActivationEvent.objects.order_by('time')
        self.assertEqual(len(events), 2)
        self.assertTrue(events[0].was_activated)
        self.assertFalse(events[1].was_activated)

    def test_entity_relationship_multiple_joins(self):
        """
        Test the case when an entity joins and leaves a relationship multiple times
        """

        # Create the relation
        entity_relation = G(EntityRelationship)
        sub_entity = entity_relation.sub_entity
        super_entity = entity_relation.super_entity

        # Delete the relationship
        entity_relation.delete()

        # Recreate the relationship
        entity_relation = G(
            EntityRelationship,
            sub_entity=sub_entity,
            super_entity=super_entity
        )

        # Delete the relationship
        entity_relation.delete()

        # Assert that we only have the correct events
        events = EntityRelationshipActivationEvent.objects.order_by('time')
        self.assertEqual(len(events), 4)
        self.assertTrue(events[0].was_activated)
        self.assertFalse(events[1].was_activated)
        self.assertTrue(events[2].was_activated)
        self.assertFalse(events[3].was_activated)
