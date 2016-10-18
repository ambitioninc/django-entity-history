CREATE OR REPLACE FUNCTION update_entity_activation_history() RETURNS trigger AS $body$
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
        entity_history_entityactivationevent
    WHERE
        entity_id = row.id
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

    -----------------------------------------------------------------
    -- Handle when an entity is created
    -----------------------------------------------------------------
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO entity_history_entityactivationevent(
            entity_id,
            time,
            was_activated
        )
        VALUES (
            NEW.id,
            CAST(CLOCK_TIMESTAMP() at time zone 'utc' AS timestamp),
            NEW.is_active
        );

    -----------------------------------------------------------------
    -- Handle when an entity was activated
    -----------------------------------------------------------------
    ELSEIF (TG_OP = 'UPDATE' AND NEW.is_active IS TRUE AND last_history_row_was_activated IS FALSE) THEN
        INSERT INTO entity_history_entityactivationevent(
            entity_id,
            time,
            was_activated
        )
        VALUES (
            NEW.id,
            CAST(CLOCK_TIMESTAMP() at time zone 'utc' AS timestamp),
            TRUE
        );

    -----------------------------------------------------------------
    -- Handle when an entity was deactivated
    -----------------------------------------------------------------
    ELSEIF (TG_OP = 'UPDATE' AND NEW.is_active IS FALSE AND last_history_row_was_activated IS TRUE) THEN
        INSERT INTO entity_history_entityactivationevent(
            entity_id,
            time,
            was_activated
        )
        VALUES (
            NEW.id,
            CAST(CLOCK_TIMESTAMP() at time zone 'utc' AS timestamp),
            FALSE
        );

    -- End the if
    END IF;

    -- Return the new row
    RETURN NEW;

-- End the body
END;
$body$
LANGUAGE plpgsql VOLATILE;
