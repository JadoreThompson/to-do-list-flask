import psycopg2
from psycopg2 import sql
import models

with psycopg2.connect(**models.conn_params) as conn:
    with conn.cursor() as cur:
        db_query = sql.SQL("""
            SELECT * FROM tasks WHERE id=6;
        """)
        cur.execute(db_query)
        rows = cur.fetchone()

        print(rows)
