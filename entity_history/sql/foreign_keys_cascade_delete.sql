DO
$body$
DECLARE
    _constraint_row RECORD;
BEGIN
    FOR _constraint_row IN (
        SELECT tc.constraint_name,
        tc.constraint_type,
        tc.table_name,
        kcu.column_name,
        tc.is_deferrable,
        tc.initially_deferred,
        rc.match_option AS match_type,

        rc.update_rule AS on_update,
        rc.delete_rule AS on_delete,
        ccu.table_name AS references_table,
        ccu.column_name AS references_column
        FROM information_schema.table_constraints tc

        LEFT JOIN information_schema.key_column_usage kcu
        ON tc.constraint_catalog = kcu.constraint_catalog
        AND tc.constraint_schema = kcu.constraint_schema
        AND tc.constraint_name = kcu.constraint_name

        LEFT JOIN information_schema.referential_constraints rc
        ON tc.constraint_catalog = rc.constraint_catalog
        AND tc.constraint_schema = rc.constraint_schema
        AND tc.constraint_name = rc.constraint_name

        LEFT JOIN information_schema.constraint_column_usage ccu
        ON rc.unique_constraint_catalog = ccu.constraint_catalog
        AND rc.unique_constraint_schema = ccu.constraint_schema
        AND rc.unique_constraint_name = ccu.constraint_name

        WHERE lower(tc.constraint_type) = 'foreign key'
        AND tc.table_name IN ('entity_history_entityactivationevent', 'entity_history_entityrelationshipactivationevent')
    )
    LOOP
        IF _constraint_row IS NOT NULL THEN
            EXECUTE 'ALTER TABLE public.' || quote_ident(_constraint_row.table_name) || ' ' ||
                'DROP CONSTRAINT ' || quote_ident(_constraint_row.constraint_name);
            EXECUTE 'ALTER TABLE public.'  || quote_ident(_constraint_row.table_name) || ' ' ||
                'ADD CONSTRAINT ' || quote_ident(_constraint_row.constraint_name) || ' ' ||
                'FOREIGN KEY (' || quote_ident(_constraint_row.column_name) || ')' || ' ' ||
                'REFERENCES public.' || quote_ident(_constraint_row.references_table) || ' ' || '(' || quote_ident(_constraint_row.references_column) || ')' || ' MATCH SIMPLE' || ' ' ||
                'ON UPDATE NO ACTION' || ' ' ||
                'ON DELETE CASCADE' || ' ' ||
                'DEFERRABLE INITIALLY DEFERRED';
        END IF;
    END LOOP;
END
$body$
