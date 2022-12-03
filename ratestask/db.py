import contextlib

import psycopg2
from flask import current_app


def get_conn():
    return psycopg2.connect(current_app.config["DB_DSN"])


@contextlib.contextmanager
def new_conn():
    conn = get_conn()
    curs = conn.cursor()
    yield curs
    conn.commit()
    curs.close()
    conn.close()
