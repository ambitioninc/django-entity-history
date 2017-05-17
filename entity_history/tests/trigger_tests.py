from django.test import TransactionTestCase
from django_dynamic_fixture import G
from entity.models import Entity, EntityRelationship

from entity_history.models import EntityActivationEvent, EntityRelationshipActivationEvent

from entity_history.sql.triggers import (
    EntityActivationTrigger,
    EntityRelationshipActivationTrigger,
    EntityRelationshipActivationImmediateTrigger
)


class EntityActivationTriggerTest(TransactionTestCase):
    def test_enable(self):
        # Enable the trigger
        EntityActivationTrigger().enable()

        # Create an entity
        G(Entity, is_active=True)

        # Assert that we have an entity activation event
        self.assertTrue(EntityActivationEvent.objects.count())

    def test_disable(self):
        # Enable the trigger
        EntityActivationTrigger().disable()

        # Create an entity
        G(Entity, is_active=True)

        # Assert that we have an entity activation event
        self.assertFalse(EntityActivationEvent.objects.count())


class EntityRelationshipActivationTriggerTest(TransactionTestCase):
    def test_enable(self):
        # Enable the trigger and assert an error is thrown
        with self.assertRaises(Exception):
            EntityRelationshipActivationTrigger().enable()

    def test_disable(self):
        # Enable the trigger
        EntityRelationshipActivationTrigger().disable()

        # Create an entity relationship
        G(EntityRelationship)

        # Assert that we do not have an entity activation event
        self.assertFalse(EntityRelationshipActivationEvent.objects.count())


class EntityRelationshipActivationImmediateTriggerTest(TransactionTestCase):
    def test_enable(self):
        # Enable the trigger
        EntityRelationshipActivationImmediateTrigger().enable()

        # Create an entity relationship
        G(EntityRelationship)

        # Assert that we have an entity activation event
        self.assertTrue(EntityRelationshipActivationEvent.objects.count())

    def test_disable(self):
        # Enable the trigger
        EntityRelationshipActivationImmediateTrigger().disable()

        # Create an entity relationship
        G(EntityRelationship)

        # Assert that we do not have an entity activation event
        self.assertFalse(EntityRelationshipActivationEvent.objects.count())
