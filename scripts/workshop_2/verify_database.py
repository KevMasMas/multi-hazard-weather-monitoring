"""Exercise the real saved-capture historical path and retain a bounded receipt.

Requires DATABASE_URL; never downloads weather data. Canonical data and two
successful runs per selected partition remain in the development database.
"""
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from ingest import _connect, _historical, _status


def main():
    with _connect() as connection:
        first=_historical(connection,'2024-01-01','2025-12-31')
        with connection.cursor() as cursor:
            cursor.execute('SELECT source_id,count(*) FROM historical_record GROUP BY source_id ORDER BY source_id')
            before=dict(cursor.fetchall())
        second=_historical(connection,'2024-01-01','2025-12-31')
        with connection.cursor() as cursor:
            cursor.execute('SELECT source_id,count(*) FROM historical_record GROUP BY source_id ORDER BY source_id')
            after=dict(cursor.fetchall())
            cursor.execute('SELECT version(), PostGIS_Full_Version()')
            database,postgis=cursor.fetchone()
            cursor.execute('SELECT count(*) FROM (SELECT source_id,source_key FROM historical_record GROUP BY source_id,source_key HAVING count(*)>1) duplicates')
            duplicates=cursor.fetchone()[0]
        assert before==after and duplicates==0
        assert [(r['read'],r['accepted'],r['rejected'],r['unchanged']) for r in second]==[(250,0,0,250),(1095,0,0,1095)]
        result=dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),
                    scope='Real saved-sample PostgreSQL load and rerun; not full historical coverage or DAG/Silver evidence.',
                    platform=platform.platform(),python=platform.python_version(),
                    database_version=database,postgis_version=postgis,
                    first_invocation=first,second_invocation=second,
                    canonical_counts_before_rerun=before,canonical_counts_after_rerun=after,
                    duplicate_business_keys=duplicates,status=_status(connection))
    path=ROOT/'workshop_2/evidence/database_verification.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(first=first,rerun=second,canonical_counts=after,duplicates=duplicates,receipt=str(path))))


if __name__=='__main__':
    main()
