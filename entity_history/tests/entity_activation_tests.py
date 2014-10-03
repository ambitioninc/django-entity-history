from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G
from entity.models import Entity

from entity_history import EntityActivationEvent


class EntityActivationTest(TestCase):
    """
    Tests that entity activation events are properly created when entities
    are activated and deactivated.
    """
    def test_entity_creation_activated(self):
        before_t = datetime.utcnow()
        e = G(Entity, is_active=True)
        after_t = datetime.utcnow()

        event = EntityActivationEvent.objects.get()
        self.assertTrue(event.was_activated)
        self.assertEquals(event.entity, e)
        self.assertTrue(before_t <= event.time <= after_t)

    def test_entity_creation_deactivated(self):
        before_t = datetime.utcnow()
        e = G(Entity, is_active=False)
        after_t = datetime.utcnow()

        event = EntityActivationEvent.objects.get()
        self.assertFalse(event.was_activated)
        self.assertEquals(event.entity, e)
        self.assertTrue(before_t <= event.time <= after_t)
