DO
$BODY$
DECLARE
   trigger_name text := (
      SELECT tgname
      FROM (pg_trigger JOIN pg_class ON tgrelid=pg_class.oid) JOIN pg_proc ON (tgfoid=pg_proc.oid)
      WHERE relname='entity_entityrelationship' AND tgname='update_entity_relationship_activation_history'
    );
BEGIN
    IF trigger_name IS NULL THEN
        CREATE CONSTRAINT TRIGGER update_entity_relationship_activation_history
        AFTER INSERT OR DELETE
        ON entity_entityrelationship
        NOT DEFERRABLE INITIALLY IMMEDIATE
        FOR EACH ROW EXECUTE PROCEDURE update_entity_relationship_activation_history();
    END IF;
END
$BODY$
