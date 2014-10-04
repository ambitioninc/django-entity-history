from django.db import models
from entity.models import Entity


class EntityActivationEvent(models.Model):
    """
    Models an event of an entity being activated or deactivated.
    """
    entity = models.ForeignKey(Entity, help_text='The entity that was activated / deactivated')
    time = models.DateTimeField(db_index=True, help_text='The time of the activation / deactivation')
    was_activated = models.BooleanField(help_text='True if the entity was activated, false otherwise')


class EntityRelationshipActivationEvent(models.Model):
    """
    Models an event of an entity relationship being activated or deactivated. Technically, entity relationships
    are either created or deleted, however, we use the terms activated and deactivated for consistency.
    """
    sub_entity = models.ForeignKey(
        Entity, related_name='+', help_text='The sub entity in the relationship that was activated / deactivated')
    super_entity = models.ForeignKey(
        Entity, related_name='+', help_text='The super entity in the relationship that was activated / deactivated')
    time = models.DateTimeField(db_index=True, help_text='The time of the activation / deactivation')
    was_activated = models.BooleanField(help_text='True if the entity was activated, false otherwise')
