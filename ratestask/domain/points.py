from typing import Dict

from ratestask import db


def get_points(codes: Dict[str, str]):
    """
    Given a map of {label: code}, returns a map of {label: path}
    """
    with db.new_conn() as conn:
        conn.execute(
            """
            SELECT code, path
            FROM points
            WHERE code = ANY(%(codes)s)
            """,
            {"codes": list(codes.values())},
        )

        points = {r[0]: r[1] for r in conn.fetchall()}
        return {label: points.get(code, None) for label, code in codes.items()}
