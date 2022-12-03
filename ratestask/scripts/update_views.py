from ratestask import create_app
from ratestask.db import new_conn


def main():
    with create_app().app_context():
        with new_conn() as conn:
            conn.execute("REFRESH MATERIALIZED VIEW region_tree")
            conn.execute("REFRESH MATERIALIZED VIEW points")


if __name__ == "__main__":
    main()
