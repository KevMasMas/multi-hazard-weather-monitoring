-- One metadata database, kept separate from the weather canonical tables.
SELECT 'CREATE DATABASE airflow OWNER weather'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname='airflow')
\gexec
