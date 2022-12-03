from typing import Dict, List, ClassVar

from pydantic import BaseModel

from ratestask import db


class Point(BaseModel):
    code: str
    path: List[str]
    kind: str

    @property
    def is_port(self):
        return self.kind == "port"

    @property
    def is_region(self):
        return self.kind == "region"

    def is_parent_of(self, other: "Point"):
        return self.code in other.path


def get_points(codes: Dict[str, str]) -> Dict[str, Point]:
    """
    Given a map of {label: code}, returns a map of {label: path}
    """
    with db.new_conn() as conn:
        conn.execute(
            """
            SELECT code, path, kind
            FROM points
            WHERE code = ANY(%(codes)s)
            """,
            {"codes": list(codes.values())},
        )

        points = {r[0]: Point(code=r[0], path=r[1], kind=r[2]) for r in conn.fetchall()}
        return {label: points.get(code, None) for label, code in codes.items()}
