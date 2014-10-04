from datetime import datetime

from django.test import TestCase
from django_dynamic_fixture import G
from entity.models import Entity

from entity_history import get_sub_entities_at_time, EntityRelationshipActivationEvent


class GetSubEntitiesAtTimeTest(TestCase):
    """
    Test the get_sub_entities_at_time function.
    """
    def test_no_events_no_input(self):
        res = get_sub_entities_at_time([], [])
        self.assertEquals(res, {})

    def test_no_events_w_input(self):
        res = get_sub_entities_at_time([1, 2], [datetime(2013, 4, 5), datetime(2013, 5, 6)])
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

        res = get_sub_entities_at_time([se.id], [datetime(2012, 4, 5), datetime(2012, 5, 6)])
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

        res = get_sub_entities_at_time([super_e.id], [datetime(2013, 2, 2), datetime(2012, 5, 6)])
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

        res = get_sub_entities_at_time([super_e.id], [datetime(2013, 2, 4)])
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

        res = get_sub_entities_at_time([super_e.id], [datetime(2013, 2, 6), datetime(2012, 5, 6)])
        self.assertEquals(res, {
            (super_e.id, datetime(2013, 2, 6)): set([sub_e.id]),
            (super_e.id, datetime(2012, 5, 6)): set(),
        })
