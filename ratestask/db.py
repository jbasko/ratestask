import contextlib

import psycopg2


def get_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="ratestask",
    )
    return conn


@contextlib.contextmanager
def new_conn():
    conn = get_conn()
    curs = conn.cursor()
    yield curs
    conn.commit()
    curs.close()
    conn.close()

