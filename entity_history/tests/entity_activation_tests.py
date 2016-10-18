from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G, N
from entity.models import Entity

from entity_history.models import EntityActivationEvent


class EntityActivationTriggerTests(TestCase):
    """
    Tests that entity activation events are properly created when entities
    are activated and deactivated. This is accomplished by a postgres database
    trigger that is installed in a data migration.
    """
    def test_bulk_create(self):
        # Create the entities
        es = [N(Entity, is_active=True) for i in range(3)]
        t1 = datetime.utcnow()
        Entity.objects.bulk_create(es)
        t2 = datetime.utcnow()
        es = list(Entity.objects.order_by('id'))

        # Check that the events exist
        events = list(EntityActivationEvent.objects.all())
        self.assertTrue(len(events), 3)
        for i in range(3):
            self.assertEquals(events[i].entity, es[i])
            self.assertTrue(t1 <= events[i].time <= t2)

    def test_bulk_create_update(self):
        es = [N(Entity, is_active=True) for i in range(3)]
        t1 = datetime.utcnow()
        Entity.objects.bulk_create(es)
        t2 = datetime.utcnow()
        es = list(Entity.objects.order_by('id'))

        Entity.objects.update(is_active=False)
        t3 = datetime.utcnow()

        events = list(EntityActivationEvent.objects.all())
        self.assertTrue(len(events), 6)
        for i in range(3):
            self.assertEquals(events[i].entity, es[i])
            self.assertTrue(t1 <= events[i].time <= t2)
            self.assertTrue(events[i].was_activated)

        # The entities deactivation order is dependent on the DB. Populate
        # all deactivated entities and verify they are the same as the entities
        deactivated = []
        for i in range(3, 6):
            self.assertTrue(t2 <= events[i].time <= t3)
            self.assertFalse(events[i].was_activated)
            deactivated.append(events[i].entity)
        self.assertEquals(set(deactivated), set(es))

    def test_entity_creation_activated(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=True)
        t2 = datetime.utcnow()

        event = EntityActivationEvent.objects.get()
        self.assertTrue(event.was_activated)
        self.assertEquals(event.entity, e)
        self.assertTrue(t1 <= event.time <= t2)

    def test_entity_creation_deactivated(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=False)
        t2 = datetime.utcnow()

        event = EntityActivationEvent.objects.get()
        self.assertFalse(event.was_activated)
        self.assertEquals(event.entity, e)
        self.assertTrue(t1 <= event.time <= t2)

    def test_update_inactive_to_active(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=False)
        t2 = datetime.utcnow()
        e.is_active = True
        e.save()
        t3 = datetime.utcnow()

        events = list(EntityActivationEvent.objects.order_by('time', 'id'))

        self.assertFalse(events[0].was_activated)
        self.assertEquals(events[0].entity, e)
        self.assertTrue(t1 <= events[0].time <= t2)

        self.assertTrue(events[1].was_activated)
        self.assertEquals(events[1].entity, e)
        self.assertTrue(t2 <= events[1].time <= t3)

    def test_update_inactive_to_active_to_active(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=False)
        t2 = datetime.utcnow()
        e.is_active = True
        e.save()
        t3 = datetime.utcnow()
        e.is_active = True
        e.save()

        events = list(EntityActivationEvent.objects.order_by('time', 'id'))

        self.assertFalse(events[0].was_activated)
        self.assertEquals(events[0].entity, e)
        self.assertTrue(t1 <= events[0].time <= t2)

        self.assertTrue(events[1].was_activated)
        self.assertEquals(events[1].entity, e)
        self.assertTrue(t2 <= events[1].time <= t3)

    def test_update_inactive_to_active_to_active_to_inactive(self):
        t1 = datetime.utcnow()
        e = G(Entity, is_active=False)
        t2 = datetime.utcnow()
        e.is_active = True
        e.save()
        t3 = datetime.utcnow()
        e.is_active = True
        e.save()
        e.is_active = False
        e.save()
        t4 = datetime.utcnow()

        events = list(EntityActivationEvent.objects.order_by('time', 'id'))

        self.assertFalse(events[0].was_activated)
        self.assertEquals(events[0].entity, e)
        self.assertTrue(t1 <= events[0].time <= t2)

        self.assertTrue(events[1].was_activated)
        self.assertEquals(events[1].entity, e)
        self.assertTrue(t2 <= events[1].time <= t3)

        self.assertFalse(events[2].was_activated)
        self.assertEquals(events[2].entity, e)
        self.assertTrue(t3 <= events[2].time <= t4)
