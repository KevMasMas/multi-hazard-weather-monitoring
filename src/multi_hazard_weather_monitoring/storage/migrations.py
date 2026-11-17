"""Apply ordered, checksum-locked SQL migrations in one transaction."""
import hashlib
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parents[3] / 'sql'


def migrate(connection, sql_dir: Path = SQL_DIR):
    if connection.autocommit:
        raise ValueError('transactional_connection_required')
    applied=[]
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(hashtextextended(current_schema() || ':weather_migrations', 0))")
            cursor.execute('''CREATE TABLE IF NOT EXISTS schema_migration (
                filename text PRIMARY KEY, sha256 char(64) NOT NULL,
                applied_at_utc timestamptz NOT NULL DEFAULT clock_timestamp())''')
            for path in sorted(sql_dir.glob('[0-9][0-9][0-9]_*.sql')):
                body=path.read_bytes()
                digest=hashlib.sha256(body).hexdigest()
                cursor.execute('SELECT sha256 FROM schema_migration WHERE filename=%s',(path.name,))
                existing=cursor.fetchone()
                if existing:
                    if existing[0].strip()!=digest:
                        raise ValueError('applied_migration_changed:'+path.name)
                    continue
                cursor.execute(body.decode('utf-8'))
                cursor.execute('INSERT INTO schema_migration(filename,sha256) VALUES (%s,%s)',(path.name,digest))
                applied.append(path.name)
        connection.commit()
        return applied
    except BaseException:
        connection.rollback()
        raise
