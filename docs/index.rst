django-entity-history: An app for tracking and reconstructing historical entity states
======================================================================================

The Django Entity History app provides the ability to track and reconstruct historical states of the `Django Entity app`_.

.. _Django Entity app: https://github.com/ambitioninc/django-entity

Django Entity provides the ability to mirror entities and sub/super relationships across entities based on the modeling of a Django application. However, the application does not maintain any information about history entity relationships, for example, when a user joined and left a group.

Basic Overview
--------------

Django Entity History tracks the following information about entities:

    1. Activation and deactivation of entities.
    2. Creation and deletion of entity relationships.

With this information, Djagno Entity History provides utilities to gather information about entities and entity groupings at various points in time. It allows some of the following example questions to be answered:

    1. Which entities were active at a point in time?
    2. Which entities were sub entities to a particular super entity at a point in time?

For the cases when it is important for an application to track history entity information, such as when entities were activated/deactivated and when entity relationships were created and removed.


Caveats
-------

Django Entity History only works with Postgres backends. This is because it installs a custom postgres database trigger to track various entity events