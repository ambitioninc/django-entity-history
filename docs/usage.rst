Usage
=====

Django Entity History comes with two primary functions - `get_entities_at_times` and `get_sub_entities_at_times`. These functions allow the user to get various historical information at provided points in time.

Getting entities at points in time
----------------------------------

Active entities at points in time can be obtained by the `get_entities_at_times` function, which has the following prototype:

.. code-block:: python

    get_entities_at_times(times, filter_by_entity_ids=None)

For example, if the user wishes to obtain all entities on January 1st and 2nd in 2011, they would issue the following code:

.. code-block:: python

    from entity_history import get_entities_at_times

    e = get_sub_entities_at_times([datetime(2011, 1, 1), datetime(2011, 1, 2)])

The `e` variable in the example is a dictionary that is keyed on times. Each key has an associated set of the entity IDs that were sub entities to the super entity. If there were no sub entities to the provided super entity, the key will still be present in the returned dictionary and point to an empty set.

The user may also filter the resulting entities by providing an iterable of entity IDs in the `filter_by_entity_ids` keyword argument.

Another approach of filtering the results is to also use the `EntityHistory` proxy model included in Django Entity History. For example,

.. code-block:: python

    from entity_history import EntityHistory

    # Filter all of the entities using any filter available in Django Entity. Then use the
    # get_entities_at_times to obtain historical information about results
    e = EntityHistory.objects.filter(id__in=[1, 2]).get_entities_at_times([datetime(2011, 1, 1), datetime(2011, 2, 1)])

The above example is equivalent to calling:

.. code-block:: python

    get_entities_at_times([datetime(2011, 1, 1), datetime(2011, 2, 1)], filter_by_entity_ids=[1, 2])

Getting sub entities at points in time
--------------------------------------

Similar to obtaining entities at points in time, sub entities at various points in time can be obtained by the `get_sub_entities_at_times` function. It has the following prototype:

.. code-block:: python

    get_sub_entities_at_times(super_entity_ids, times, filter_by_entity_ids=None)

For example, if the user wishes to obtain all sub entities on January 1st, 2011 to the super entity with ID 1, they would issue the following statement:

.. code-block:: python

    from entity_history import get_sub_entities_at_times

    se = get_sub_entities_at_times([1], [datetime(2011, 1, 1)])

The `se` variable in the example is a dictionary that is keyed on `(super_entity_id, time)` tuples. Each key has an associated set of the entity IDs that were sub entities to the super entity. If there were no sub entities to the provided super entity, the key will still be present in the returned dictionary and point to an empty set.

If the user wishes to filter out entities from the results, they have the option to pass an iterable of entity IDs to the `filter_by_entity_ids` keyword argument.

The user can also perform entity filtering using the `EntityHistory` proxy model that comes with Django Entity History and filter out entity results in the following manner:

.. code-block:: python

    from entity_history import EntityHistory

    # Filter all of the entities using any filter available in Django Entity. Then use the
    # get_sub_entities_at_times to obtain historical information about results
    se = EntityHistory.objects.filter(id__in=[1, 2]).get_sub_entities_at_times([3], [datetime(2011, 1, 1), datetime(2011, 2, 1)])

The above example is equivalent to calling:

.. code-block:: python

    get_sub_entities_at_times([3], [datetime(2011, 1, 1), datetime(2011, 2, 1)], filter_by_entity_ids=[1, 2])

Note that `EntityHistory` has a similar interface to `Entity` in that it only filters active entities by default. If one wishes to query for all active and inactive entities, use `EntityHistory.all_objects.all()`.
