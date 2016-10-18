from django.test import TransactionTestCase
from django_dynamic_fixture import G
from entity.models import Entity, EntityRelationship
from mock import patch

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
        # Enable the trigger
        EntityRelationshipActivationTrigger().enable()

        # Create an entity
        G(EntityRelationship)

        # Assert that we have an entity activation event
        self.assertTrue(EntityRelationshipActivationEvent.objects.count())

    def test_disable(self):
        # Enable the trigger
        EntityRelationshipActivationTrigger().disable()

        # Create an entity relationship
        G(EntityRelationship)

        # Assert that we have an entity activation event
        self.assertFalse(EntityRelationshipActivationEvent.objects.count())


class EntityRelationshipActivationImmediateTriggerTest(TransactionTestCase):
    @patch('entity_history.sql.triggers.sys.argv', return_value=[])
    def test_enable(self, mock_sys):
        # Enable the trigger
        with self.assertRaises(Exception):
            EntityRelationshipActivationImmediateTrigger().enable()

    def test_enable_in_testing(self):
        # Enable the trigger
        EntityRelationshipActivationImmediateTrigger().enable()

    def test_disable(self):
        # Enable the trigger
        EntityRelationshipActivationImmediateTrigger().disable()
