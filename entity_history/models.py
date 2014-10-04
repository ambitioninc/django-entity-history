from django.db import models
from entity.models import Entity


class EntityActivationEvent(models.Model):
    """
    Models an event of an entity being activated or deactivated.
    """
    entity = models.ForeignKey(Entity, help_text='The entity that was activated / deactivated')
    time = models.DateTimeField(db_index=True, help_text='The time of the activation / deactivation')
    was_activated = models.BooleanField(help_text='True if the entity was activated, false otherwise')
