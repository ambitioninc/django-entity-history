from django.db import models
from entity.models import Entity, EntityQuerySet, AllEntityManager


class EntityActivationEvent(models.Model):
    """
    Models an event of an entity being activated or deactivated.
    """
    entity = models.ForeignKey(Entity, help_text='The entity that was activated / deactivated')
    time = models.DateTimeField(db_index=True, help_text='The time of the activation / deactivation')
    was_activated = models.BooleanField(default=None, help_text='True if the entity was activated, false otherwise')

    class Meta:
        app_label = 'entity_history'


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
    was_activated = models.BooleanField(default=None, help_text='True if the entity was activated, false otherwise')

    class Meta:
        app_label = 'entity_history'


def get_sub_entities_at_times(super_entity_ids, times, filter_by_entity_ids=None):
    """
    Constructs the sub entities of super entities at points in time.

    :param super_entity_ids: An iterable of super entity ids
    :param times: An iterable of datetime objects
    :param filter_by_entity_ids: An iterable of entity ids over which to filter the results
    :returns: A dictionary keyed on (super_entity_id, time) tuples. Each key has a set of all entity ids that were sub
       entities of the super entity during that time.
    """
    er_events = EntityRelationshipActivationEvent.objects.filter(super_entity_id__in=super_entity_ids).order_by('time')
    if filter_by_entity_ids:
        er_events = er_events.filter(sub_entity_id__in=filter_by_entity_ids)

    ers = {
        (se_id, t): set()
        for se_id in super_entity_ids
        for t in times
    }

    for t in times:
        # Traverse the entity relationship events in ascending time, keeping track of if a sub entity was in a
        # relationship before time t
        for er_event in [er for er in er_events if er.time < t]:
            if er_event.was_activated:
                ers[(er_event.super_entity_id, t)].add(er_event.sub_entity_id)
            else:
                ers[(er_event.super_entity_id, t)].discard(er_event.sub_entity_id)

    return ers


def get_entities_at_times(times, filter_by_entity_ids=None):
    """
    Constructs the entities that were active at points in time.

    :param times: An iterable of datetime objects
    :param filter_by_entity_ids: An iterable of entity ids over which to filter the results
    :returns: A dictionary keyed on time values. Each key has a set of all entity ids that were active at the time.
    """
    e_events = EntityActivationEvent.objects.order_by('time')
    if filter_by_entity_ids:
        e_events = e_events.filter(entity_id__in=filter_by_entity_ids)

    es = {
        t: set()
        for t in times
    }

    for t in times:
        # Traverse the entity events in ascending time, keeping track of if an entity was active before time t
        for e_event in [e for e in e_events if e.time < t]:
            if e_event.was_activated:
                es[t].add(e_event.entity_id)
            else:
                es[t].discard(e_event.entity_id)

    return es


class EntityHistoryQuerySet(EntityQuerySet):
    """
    A queryset that wraps around the get_sub_entities_at_times and get_entities_at_times functions.
    """
    def get_sub_entities_at_times(self, super_entity_ids, times):
        return get_sub_entities_at_times(
            super_entity_ids, times, filter_by_entity_ids=self.values_list('id', flat=True))

    def get_entities_at_times(self, times):
        return get_entities_at_times(times, filter_by_entity_ids=self.values_list('id', flat=True))


class AllEntityHistoryManager(AllEntityManager):
    def get_queryset(self):
        return EntityHistoryQuerySet(self.model)

    def get_sub_entities_at_times(self, super_entity_ids, times):
        return self.get_queryset().get_sub_entities_at_times(super_entity_ids, times)

    def get_entities_at_times(self, times):
        return self.get_queryset().get_entities_at_times(times)


class ActiveEntityHistoryManager(AllEntityHistoryManager):
    """
    The default 'objects' on the EntityHistory model. This manager restricts all Entity queries to happen over active
    entities.
    """
    def get_queryset(self):
        return EntityHistoryQuerySet(self.model).active()


class EntityHistory(Entity):
    """
    A proxy model for entities that overrides the default model manager. This model manager provides additional
    functionality to query entities and entity relationships at points in time.
    """
    class Meta:
        proxy = True

    objects = ActiveEntityHistoryManager()
    all_objects = AllEntityHistoryManager()
