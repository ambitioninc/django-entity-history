CREATE OR REPLACE FUNCTION update_entity_relationship_activation_history() RETURNS trigger AS $body$
DECLARE
    row RECORD;
    last_history_row RECORD;
    last_history_row_was_activated BOOL;
BEGIN
    -----------------------------------------------------------------
    -- Default values
    -----------------------------------------------------------------
    last_history_row_was_activated = FALSE;
    last_history_row = NULL;
    row = NULL;

    -----------------------------------------------------------------
    -- Get the row
    -----------------------------------------------------------------
    IF (TG_OP = 'INSERT') THEN
        row = NEW;
    ELSE
        row = OLD;
    END IF;

    -----------------------------------------------------------------
    -- Get the last history row that exists
    -----------------------------------------------------------------
    SELECT
        *
    INTO
        last_history_row
    FROM
        entity_history_entityrelationshipactivationevent
    WHERE
        sub_entity_id = row.sub_entity_id
    AND
        super_entity_id = row.super_entity_id
    ORDER BY
        time DESC
    LIMIT
        1;

    -----------------------------------------------------------------
    -- Compute what the last history row was_activated flag was
    -----------------------------------------------------------------
    IF last_history_row IS NOT NULL THEN
        last_history_row_was_activated = last_history_row.was_activated;
    END IF;

    ----------------------------------------------------------------------------------------------------
    -- Handle the case where this is a new relationship, and the last row was not found or was active
    ----------------------------------------------------------------------------------------------------
    IF (TG_OP = 'INSERT' AND last_history_row_was_activated IS FALSE) THEN
        INSERT INTO entity_history_entityrelationshipactivationevent(
            sub_entity_id,
            super_entity_id,
            time,
            was_activated
        )
        VALUES (
            NEW.sub_entity_id,
            NEW.super_entity_id,
            CAST(CLOCK_TIMESTAMP() at time zone 'utc' AS timestamp),
            TRUE
        );
    END IF;

    ----------------------------------------------------------------------------------------------------
    -- Handle the case where the relationship is removed.
    ----------------------------------------------------------------------------------------------------
    IF (TG_OP = 'DELETE' AND last_history_row_was_activated IS TRUE) THEN
        INSERT INTO entity_history_entityrelationshipactivationevent(
            sub_entity_id,
            super_entity_id,
            time,
            was_activated
        )
        VALUES (
            OLD.sub_entity_id,
            OLD.super_entity_id,
            CAST(CLOCK_TIMESTAMP() at time zone 'utc' AS timestamp),
            FALSE
        );
    END IF;
    RETURN NEW;
END;
$body$
LANGUAGE plpgsql VOLATILE;
