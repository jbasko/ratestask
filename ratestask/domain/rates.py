import datetime as dt

from ratestask import db
from ratestask.domain.points import Point

RATES_QUERY = """
    SELECT
        pr.day,
        CASE WHEN COUNT(*) >= 3 THEN ROUND(AVG(pr.price))
        ELSE NULL END
        FROM prices pr
    LEFT JOIN points orig ON pr.orig_code = orig.code
    LEFT JOIN points dest ON pr.dest_code = dest.code
    WHERE
    %(origin)s = ANY(orig.path)
    AND 
    %(destination)s = ANY(dest.path)
    AND pr.day BETWEEN %(date_from)s AND %(date_to)s
    AND
        -- [CAVEAT-01] - deal with origin and destination being regions in the same tree.
        CASE WHEN %(exclude)s IS NOT NULL THEN NOT (%(exclude)s = ANY(orig.path) AND %(exclude)s = ANY(dest.path))
        ELSE TRUE END
    GROUP by pr.day
"""


def iter_average_rate_by_day(date_from: dt.date, date_to: dt.date, origin: Point, destination: Point):
    dates_range = [
        date_from + dt.timedelta(days=x)
        for x in range((date_to - date_from).days + 1)
    ]

    exclude = None
    if origin.is_region and destination.is_region:
        # [CAVEAT-01] - deal with origin and destination being regions in the same tree.
        if destination.is_parent_of(origin):
            # must exclude any prices within origin region
            exclude = origin.code
        elif origin.is_parent_of(destination):
            # must exclude any prices within destination region
            exclude = destination.code

    with db.new_conn() as conn:
        conn.execute(RATES_QUERY, {
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "origin": origin.code,
            "destination": destination.code,
            "exclude": exclude,
        })

        by_dates = {
            r[0]: int(r[1]) if r[1] else None
            for r in conn.fetchall()
        }

        for d in dates_range:
            yield d, by_dates.get(d, None)
