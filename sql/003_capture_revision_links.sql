-- Pin each per-run sighting to the immutable accepted revision it saw.
ALTER TABLE record_capture_link ADD COLUMN IF NOT EXISTS revision_id bigint
    REFERENCES historical_record_revision(revision_id);
UPDATE record_capture_link l SET revision_id=(
    SELECT r.revision_id FROM historical_record_revision r
    WHERE r.record_id=l.record_id AND r.run_id<=l.run_id
    ORDER BY r.run_id DESC LIMIT 1
) WHERE revision_id IS NULL;
ALTER TABLE record_capture_link ALTER COLUMN revision_id SET NOT NULL;
