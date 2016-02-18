from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G
from entity.models import Entity

from entity_history.models import (
    get_sub_entities_at_times, EntityRelationshipActivationEvent, get_entities_at_times, EntityActivationEvent,
    EntityHistory
)


class EntityManagerTest(TestCase):
    def test_all_entity_history_manager_returns_active_and_inactive(self):
        active_e = G(EntityHistory, is_active=True)
        inactive_e = G(EntityHistory, is_active=False)
        self.assertEquals(set([active_e, inactive_e]), set(EntityHistory.all_objects.all()))

    def test_active_entity_history_manager_returns_active(self):
        active_e = G(EntityHistory, is_active=True)
        G(Entity, is_active=False)
        self.assertEquals(set([active_e]), set(EntityHistory.objects.all()))


class GetSubEntitiesAtTimesTest(TestCase):
    """
    Test the get_sub_entities_at_times function.
    """
    def test_no_events_no_input(self):
        res = get_sub_entities_at_times([], [])
        self.assertEquals(res, {})

    def test_no_events_w_input(self):
        res = get_sub_entities_at_times([1, 2], [datetime(2013, 4, 5), datetime(2013, 5, 6)])
        self.assertEquals(res, {
            (1, datetime(2013, 4, 5)): set(),
            (1, datetime(2013, 5, 6)): set(),
            (2, datetime(2013, 4, 5)): set(),
            (2, datetime(2013, 5, 6)): set(),
        })

    def test_w_events_no_results(self):
        se = G(Entity)
        G(EntityRelationshipActivationEvent, was_activated=True, super_entity=se, time=datetime(2013, 2, 1))
        G(EntityRelationshipActivationEvent, was_activated=False, super_entity=se, time=datetime(2013, 2, 2))

        res = get_sub_entities_at_times([se.id], [datetime(2012, 4, 5), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            (se.id, datetime(2012, 4, 5)): set(),
            (se.id, datetime(2012, 5, 6)): set(),
        })

    def test_w_events_one_sub_e_returned(self):
        super_e = G(Entity)
        sub_e = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 3))

        res = get_sub_entities_at_times([super_e.id], [datetime(2013, 2, 2), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 2)): set([sub_e.id]),
            (super_e.id, datetime(2012, 5, 6)): set(),
        })

    def test_w_events_sub_entity_deactivated_before_date(self):
        super_e = G(Entity)
        sub_e = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 3))

        res = get_sub_entities_at_times([super_e.id], [datetime(2013, 2, 4)])
        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 4)): set(),
        })

    def test_w_mulitple_activation_events_one_sub_e_returned(self):
        super_e = G(Entity)
        sub_e = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 3))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 2, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e,
            time=datetime(2013, 3, 4, 12))

        res = get_sub_entities_at_times([super_e.id], [datetime(2013, 2, 6), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 6)): set([sub_e.id]),
            (super_e.id, datetime(2012, 5, 6)): set(),
        })

    def test_w_mulitple_activation_events_mulitple_sub_e_returned(self):
        super_e = G(Entity)
        sub_e1 = G(Entity)
        sub_e2 = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 3))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 3, 4, 12))

        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 20))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 13))

        res = get_sub_entities_at_times(
            [super_e.id], [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 2)): set([sub_e1.id]),
            (super_e.id, datetime(2013, 2, 4, 13)): set([sub_e1.id, sub_e2.id]),
            (super_e.id, datetime(2013, 3, 5)): set([sub_e2.id]),
        })

    def test_w_mulitple_activation_events_mulitple_sub_e_returned_w_filter(self):
        super_e = G(Entity)
        sub_e1 = G(Entity)
        sub_e2 = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 3))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 3, 4, 12))

        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 20))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 13))

        res = get_sub_entities_at_times(
            [super_e.id], [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)],
            filter_by_entity_ids=[sub_e2.id])

        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 2)): set(),
            (super_e.id, datetime(2013, 2, 4, 13)): set([sub_e2.id]),
            (super_e.id, datetime(2013, 3, 5)): set([sub_e2.id]),
        })

    def test_w_mulitple_activation_events_mulitple_sub_e_returned_w_queryset_filter(self):
        super_e = G(Entity)
        sub_e1 = G(Entity)
        sub_e2 = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 3))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 3, 4, 12))

        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 20))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 13))

        res = EntityHistory.objects.filter(id=sub_e2.id).get_sub_entities_at_times(
            [super_e.id], [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 2)): set(),
            (super_e.id, datetime(2013, 2, 4, 13)): set([sub_e2.id]),
            (super_e.id, datetime(2013, 3, 5)): set([sub_e2.id]),
        })

    def test_w_mulitple_activation_events_mulitple_sub_e_returned_w_manager(self):
        super_e = G(Entity)
        sub_e1 = G(Entity)
        sub_e2 = G(Entity)
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 1))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 3))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 2, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e1,
            time=datetime(2013, 3, 4, 12))

        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 2, 20))
        G(
            EntityRelationshipActivationEvent, was_activated=False, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 12))
        G(
            EntityRelationshipActivationEvent, was_activated=True, super_entity=super_e, sub_entity=sub_e2,
            time=datetime(2013, 3, 4, 13))

        res = EntityHistory.objects.get_sub_entities_at_times(
            [super_e.id], [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 2)): set([sub_e1.id]),
            (super_e.id, datetime(2013, 2, 4, 13)): set([sub_e1.id, sub_e2.id]),
            (super_e.id, datetime(2013, 3, 5)): set([sub_e2.id]),
        })

    def test_w_mulitple_activation_events_mulitple_super_e_and_sub_e_returned(self):
        super_e1 = G(Entity)
        super_e2 = G(Entity)
        sub_e1 = G(Entity)
        sub_e2 = G(Entity)
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

        res = get_sub_entities_at_times(
            [super_e1.id, super_e2.id], [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            (super_e1.id, datetime(2013, 2, 2)): set([sub_e1.id]),
            (super_e1.id, datetime(2013, 2, 4, 13)): set([sub_e1.id, sub_e2.id]),
            (super_e1.id, datetime(2013, 3, 5)): set([sub_e2.id]),
            (super_e2.id, datetime(2013, 2, 2)): set([sub_e1.id, sub_e2.id]),
            (super_e2.id, datetime(2013, 2, 4, 13)): set([sub_e1.id, sub_e2.id]),
            (super_e2.id, datetime(2013, 3, 5)): set([sub_e1.id, sub_e2.id]),
        })


class GetEntitiesAtTimeTest(TestCase):
    """
    Test the get_entities_at_times function.
    """
    def test_no_events_no_input(self):
        res = get_entities_at_times([])
        self.assertEquals(res, {})

    def test_no_events_w_input(self):
        res = get_entities_at_times([datetime(2013, 4, 5), datetime(2013, 5, 6)])
        self.assertEquals(res, {
            datetime(2013, 4, 5): set(),
            datetime(2013, 5, 6): set(),
            datetime(2013, 4, 5): set(),
            datetime(2013, 5, 6): set(),
        })

    def test_w_events_no_results(self):
        e = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e, time=datetime(2013, 2, 2))

        res = get_entities_at_times([datetime(2012, 4, 5), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            datetime(2012, 4, 5): set(),
            datetime(2012, 5, 6): set(),
        })

    def test_w_events_one_e_returned(self):
        e = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e, time=datetime(2013, 2, 3))

        res = get_entities_at_times([datetime(2013, 2, 2), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            datetime(2013, 2, 2): set([e.id]),
            datetime(2012, 5, 6): set(),
        })

    def test_w_events_entity_deactivated_before_date(self):
        e = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e, time=datetime(2013, 2, 3))

        res = get_entities_at_times([datetime(2013, 2, 4)])
        self.assertEquals(res, {
            datetime(2013, 2, 4): set(),
        })

    def test_w_mulitple_activation_events_one_e_returned(self):
        e = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e, time=datetime(2013, 2, 3))
        G(EntityActivationEvent, was_activated=False, entity=e, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=True, entity=e, time=datetime(2013, 2, 4, 12))
        G(EntityActivationEvent, was_activated=False, entity=e, time=datetime(2013, 3, 4, 12))

        res = get_entities_at_times([datetime(2013, 2, 6), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            datetime(2013, 2, 6): set([e.id]),
            datetime(2012, 5, 6): set(),
        })

    def test_w_mulitple_activation_events_mulitple_e_returned(self):
        e1 = G(Entity)
        e2 = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 3))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 4, 12))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 3, 4, 12))

        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 2, 20))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 3, 4))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 12))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 13))

        res = get_entities_at_times([datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            datetime(2013, 2, 2): set([e1.id]),
            datetime(2013, 2, 4, 13): set([e1.id, e2.id]),
            datetime(2013, 3, 5): set([e2.id]),
        })

    def test_w_mulitple_activation_events_mulitple_e_returned_w_filter(self):
        e1 = G(Entity)
        e2 = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 3))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 4, 12))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 3, 4, 12))

        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 2, 20))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 3, 4))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 12))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 13))

        res = get_entities_at_times(
            [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)],
            filter_by_entity_ids=[e1.id])

        self.assertEquals(res, {
            datetime(2013, 2, 2): set([e1.id]),
            datetime(2013, 2, 4, 13): set([e1.id]),
            datetime(2013, 3, 5): set(),
        })

    def test_w_mulitple_activation_events_mulitple_e_returned_w_queryset_filter(self):
        e1 = G(Entity)
        e2 = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 3))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 4, 12))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 3, 4, 12))

        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 2, 20))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 3, 4))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 12))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 13))

        res = EntityHistory.objects.filter(id=e1.id).get_entities_at_times(
            [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            datetime(2013, 2, 2): set([e1.id]),
            datetime(2013, 2, 4, 13): set([e1.id]),
            datetime(2013, 3, 5): set(),
        })

    def test_w_mulitple_activation_events_mulitple_e_returned_w_manager(self):
        e1 = G(Entity)
        e2 = G(Entity)
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 1))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 3))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=True, entity=e1, time=datetime(2013, 2, 4, 12))
        G(EntityActivationEvent, was_activated=False, entity=e1, time=datetime(2013, 3, 4, 12))

        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 2, 4))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 2, 20))
        G(EntityActivationEvent, was_activated=False, entity=e2, time=datetime(2013, 3, 4))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 12))
        G(EntityActivationEvent, was_activated=True, entity=e2, time=datetime(2013, 3, 4, 13))

        res = EntityHistory.objects.get_entities_at_times(
            [datetime(2013, 2, 2), datetime(2013, 2, 4, 13), datetime(2013, 3, 5)])

        self.assertEquals(res, {
            datetime(2013, 2, 2): set([e1.id]),
            datetime(2013, 2, 4, 13): set([e1.id, e2.id]),
            datetime(2013, 3, 5): set([e2.id]),
        })
